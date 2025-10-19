from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter("corvi_http_requests_total", "Total HTTP requests", ["method","endpoint","status"]) 
REQUEST_LATENCY = Histogram("corvi_http_request_duration_seconds", "HTTP request latency", ["endpoint"])
