import click, os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from corvi_api.models.subscription import FeatureFlag, UsageQuota, Subscription, SubscriptionTierEnum
from corvi_api.models.user import User, Org, Membership, RoleEnum
from corvi_api.security import get_password_hash

@click.group()
def cli():
    pass

@cli.command()
def seed_demo():
    url = os.getenv("DATABASE_URL", "postgresql+psycopg2://corvi:corvi@postgres:5432/corvi")
    eng = create_engine(url); Session = sessionmaker(bind=eng); db = Session()
    org = Org(name="DemoOrg"); db.add(org); db.flush()
    user = User(email="demo@corvi.ai", hashed_password=get_password_hash("demo"), default_org_id=org.id)
    db.add(user); db.add(Membership(user_id=user.id, org_id=org.id, role=RoleEnum.owner))
    db.add(Subscription(org_id=org.id, tier=SubscriptionTierEnum.freemium))
    db.add(UsageQuota(org_id=org.id, key="experiments_per_month", limit=10, used=0))
    db.commit(); print("Seeded demo user demo@corvi.ai / demo")

if __name__ == "__main__":
    cli()
