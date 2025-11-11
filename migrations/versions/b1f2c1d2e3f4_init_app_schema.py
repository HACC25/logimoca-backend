"""init app schema (public only)

Revision ID: b1f2c1d2e3f4
Revises: 
Create Date: 2025-11-10 00:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b1f2c1d2e3f4'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # sectors
    op.create_table(
        'sectors',
        sa.Column('id', sa.String(length=10), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('icon_url', sa.String(length=500)),
        sa.Column('pathway_url', sa.String(length=500), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
    )

    # institutions
    op.create_table(
        'institutions',
        sa.Column('id', sa.String(length=20), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('type', sa.String(length=20), nullable=False),
        sa.Column('location', sa.String(length=50), nullable=False),
        sa.Column('campus', sa.String(length=100)),
        sa.Column('website_url', sa.String(length=500), nullable=False),
        sa.Column('contact_email', sa.String(length=100)),
        sa.Column('latitude', sa.Float()),
        sa.Column('longitude', sa.Float()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
    )

    # programs
    op.create_table(
        'programs',
        sa.Column('id', sa.String(length=50), primary_key=True, nullable=False),
        sa.Column('sector_id', sa.String(length=10), sa.ForeignKey('sectors.id', ondelete='CASCADE'), nullable=False),
        sa.Column('institution_id', sa.String(length=20), sa.ForeignKey('institutions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(length=500), nullable=False),
        sa.Column('degree_type', sa.String(length=50), nullable=False),
        sa.Column('duration_years', sa.Float(), nullable=False),
        sa.Column('total_credits', sa.Integer(), nullable=False),
        sa.Column('cost_per_credit', sa.Float(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('program_url', sa.String(length=500), nullable=False),
        sa.Column('prerequisites', sa.JSON(), server_default=sa.text("'[]'::json"), nullable=False),
        sa.Column('delivery_modes', sa.JSON(), server_default=sa.text("'[]'::json"), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
    )
    op.create_index('idx_program_sector', 'programs', ['sector_id'])
    op.create_index('idx_program_duration', 'programs', ['duration_years'])

    # occupation extension table
    op.create_table(
        'occupation',
        sa.Column('onet_code', sa.String(length=10), primary_key=True, nullable=False),
        sa.Column('median_annual_wage', sa.Float()),
        sa.Column('employment_outlook', sa.String(length=50), nullable=False),
        sa.Column('job_zone', sa.Integer(), nullable=False),
        sa.Column('interest_codes', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'::jsonb"), nullable=False),
        sa.Column('interest_scores', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), nullable=False),
        sa.Column('top_skills', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'::jsonb"), nullable=False),
        sa.Column('onet_url', sa.String(length=500), nullable=False),
        sa.Column('last_updated', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        sa.ForeignKeyConstraint(['onet_code'], ['onet.occupation_data.onetsoc_code'])
    )
    op.create_index('idx_occupation_interest', 'occupation', ['interest_codes'], postgresql_using='gin')
    op.create_index('idx_occupation_job_zone', 'occupation', ['job_zone'])

    # interest codes
    op.create_table(
        'interest_codes',
        sa.Column('code', sa.String(length=1), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('color_hex', sa.String(length=7), nullable=False),
        sa.Column('job_tasks', sa.Text(), nullable=False),
        sa.Column('work_values', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
    )

    # app skills
    op.create_table(
        'app_skills',
        sa.Column('onet_element_id', sa.String(length=20), primary_key=True, nullable=False),
        sa.Column('task_statement', sa.Text(), nullable=False),
        sa.Column('anchor_low', sa.Text(), nullable=False),
        sa.Column('anchor_high', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        sa.ForeignKeyConstraint(['onet_element_id'], ['onet.content_model_reference.element_id'])
    )

    # program ↔ occupation association
    op.create_table(
        'program_occupation_association',
        sa.Column('program_id', sa.String(length=50), nullable=False),
        sa.Column('occupation_onet_code', sa.String(length=10), nullable=False),
        sa.ForeignKeyConstraint(['program_id'], ['programs.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['occupation_onet_code'], ['occupation.onet_code'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('program_id', 'occupation_onet_code')
    )


def downgrade() -> None:
    op.drop_table('program_occupation_association')
    op.drop_table('app_skills')
    op.drop_table('interest_codes')
    op.drop_index('idx_occupation_job_zone', table_name='occupation')
    op.drop_index('idx_occupation_interest', table_name='occupation')
    op.drop_table('occupation')
    op.drop_index('idx_program_duration', table_name='programs')
    op.drop_index('idx_program_sector', table_name='programs')
    op.drop_table('programs')
    op.drop_table('institutions')
    op.drop_table('sectors')
