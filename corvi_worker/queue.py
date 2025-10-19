import json, time
import pika, redis
from .config import settings

class QueueConsumer:
    def consume(self, handler):
        if settings.QUEUE_BACKEND == "rabbitmq":
            params = pika.URLParameters(settings.RABBITMQ_URL)
            # Napraw pusty vhost (RabbitMQ wymaga '/')
            if not params.virtual_host:
                params.virtual_host = '/'
            conn = pika.BlockingConnection(params)
            ch = conn.channel(); ch.queue_declare(queue="corvi_jobs", durable=True)
            for method, properties, body in ch.consume("corvi_jobs", inactivity_timeout=1):
                if body:
                    job = json.loads(body)
                    handler(job)
                    ch.basic_ack(method.delivery_tag)
        else:
            r = redis.Redis.from_url(settings.REDIS_URL)
            while True:
                item = r.brpop("corvi_jobs", timeout=1)
                if not item:
                    time.sleep(0.1); continue
                _, body = item
                job = json.loads(body)
                handler(job)