from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('orgs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, unique=True)
    )
    op.create_table('users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String, unique=True),
        sa.Column('hashed_password', sa.String),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('default_org_id', sa.Integer)
    )
    op.create_table('memberships',
        sa.Column('user_id', sa.Integer),
        sa.Column('org_id', sa.Integer),
        sa.Column('role', sa.Enum('viewer','member','admin','owner', name='roleenum')),
        sa.PrimaryKeyConstraint('user_id','org_id')
    )
    op.create_table('subscriptions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('org_id', sa.Integer, unique=True),
        sa.Column('tier', sa.Enum('freemium','premium_basic','premium_pro','enterprise', name='subscriptiontierenum'))
    )
    op.create_table('feature_flags',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('org_id', sa.Integer),
        sa.Column('key', sa.String),
        sa.Column('enabled', sa.Boolean)
    )
    op.create_table('usage_quotas',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('org_id', sa.Integer),
        sa.Column('key', sa.String),
        sa.Column('limit', sa.Integer),
        sa.Column('used', sa.Integer)
    )
    op.create_table('projects',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('org_id', sa.Integer),
        sa.Column('name', sa.String)
    )
    op.create_table('datasets',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('project_id', sa.Integer),
        sa.Column('path', sa.String),
        sa.Column('rows', sa.Integer),
        sa.Column('cols', sa.Integer),
        sa.Column('target', sa.String),
        sa.Column('format', sa.String)
    )
    op.create_table('experiments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('project_id', sa.Integer),
        sa.Column('name', sa.String),
        sa.Column('algorithm', sa.Enum('grid','random','corvi_opt', name='algoenum')),
        sa.Column('backend', sa.Enum('local','ray', name='backendenum')),
        sa.Column('space', sa.JSON),
        sa.Column('status', sa.String),
        sa.Column('best_metric', sa.String),
        sa.Column('best_value', sa.String)
    )
    op.create_table('trials',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('experiment_id', sa.Integer),
        sa.Column('params', sa.JSON),
        sa.Column('status', sa.String),
        sa.Column('value', sa.String)
    )
    op.create_table('metrics',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('experiment_id', sa.Integer),
        sa.Column('trial_id', sa.Integer),
        sa.Column('key', sa.String),
        sa.Column('value', sa.Float),
        sa.Column('step', sa.Integer)
    )
    op.create_table('artifacts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('experiment_id', sa.Integer),
        sa.Column('trial_id', sa.Integer),
        sa.Column('path', sa.String),
        sa.Column('kind', sa.String)
    )
    op.create_table('roi_formulas',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('project_id', sa.Integer),
        sa.Column('formula', sa.String),
        sa.Column('baseline', sa.Float),
        sa.Column('business_factor', sa.Float)
    )
    op.create_table('jobs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('experiment_id', sa.Integer),
        sa.Column('kind', sa.String),
        sa.Column('payload', sa.JSON),
        sa.Column('status', sa.String),
        sa.Column('attempts', sa.Integer)
    )
    op.create_table('api_keys',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('org_id', sa.Integer),
        sa.Column('name', sa.String),
        sa.Column('key', sa.String)
    )
    op.create_table('audit_logs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('actor', sa.String),
        sa.Column('action', sa.String),
        sa.Column('entity', sa.String),
        sa.Column('entity_id', sa.String),
        sa.Column('details', sa.JSON)
    )

def downgrade():
    op.drop_table('audit_logs')
    op.drop_table('api_keys')
    op.drop_table('jobs')
    op.drop_table('roi_formulas')
    op.drop_table('artifacts')
    op.drop_table('metrics')
    op.drop_table('trials')
    op.drop_table('experiments')
    op.drop_table('datasets')
    op.drop_table('projects')
    op.drop_table('usage_quotas')
    op.drop_table('feature_flags')
    op.drop_table('subscriptions')
    op.drop_table('memberships')
    op.drop_table('users')
    op.drop_table('orgs')
