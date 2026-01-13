"""create initial tables

Revision ID: 001
Revises: 
Create Date: 2026-01-13 16:11:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create configurations table
    op.create_table('configurations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('language', sa.String(length=10), nullable=False),
        sa.Column('quality_level', sa.Enum('RAPIDO', 'PROFESIONAL', 'ELITE', name='qualitylevel'), nullable=False),
        sa.Column('llm_provider', sa.String(length=50), nullable=True),
        sa.Column('llm_model', sa.String(length=100), nullable=True),
        sa.Column('llm_api_key_encrypted', sa.Text(), nullable=True),
        sa.Column('image_provider', sa.String(length=50), nullable=True),
        sa.Column('image_model', sa.String(length=100), nullable=True),
        sa.Column('image_api_key_encrypted', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create products table
    op.create_table('products',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('currency', sa.String(length=3), nullable=True),
        sa.Column('key_features', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('benefits', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('keywords', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('target_audience', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create product_images table
    op.create_table('product_images',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('image_type', sa.Enum('PRODUCT', 'SERVICE', 'LOGO', 'GENERATED', 'VARIANT', 'CAROUSEL_ITEM', 'FUSED', 'WATERMARKED', name='imagetype'), nullable=False),
        sa.Column('file_path', sa.Text(), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('width', sa.Integer(), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create generations table
    op.create_table('generations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('platforms', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('tone', sa.String(length=50), nullable=True),
        sa.Column('length', sa.String(length=20), nullable=True),
        sa.Column('use_emojis', sa.Boolean(), nullable=True),
        sa.Column('cta', sa.String(length=255), nullable=True),
        sa.Column('image_options', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('quality_level', sa.Enum('RAPIDO', 'PROFESIONAL', 'ELITE', name='qualitylevel'), nullable=True),
        sa.Column('llm_used', sa.String(length=100), nullable=True),
        sa.Column('image_model_used', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create copies table
    op.create_table('copies',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('generation_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('platform', sa.String(length=50), nullable=True),
        sa.Column('variant_number', sa.Integer(), nullable=True),
        sa.Column('copy_text', sa.Text(), nullable=False),
        sa.Column('is_favorite', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['generation_id'], ['generations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create generated_images table
    op.create_table('generated_images',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('generation_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('image_type', sa.Enum('PRODUCT', 'SERVICE', 'LOGO', 'GENERATED', 'VARIANT', 'CAROUSEL_ITEM', 'FUSED', 'WATERMARKED', name='imagetype'), nullable=False),
        sa.Column('platform', sa.String(length=50), nullable=True),
        sa.Column('file_path', sa.Text(), nullable=False),
        sa.Column('width', sa.Integer(), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),
        sa.Column('variant_number', sa.Integer(), nullable=True),
        sa.Column('processing_options', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('is_favorite', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['generation_id'], ['generations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create history table
    op.create_table('history',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('generation_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('action', sa.String(length=50), nullable=True),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['generation_id'], ['generations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('history')
    op.drop_table('generated_images')
    op.drop_table('copies')
    op.drop_table('generations')
    op.drop_table('product_images')
    op.drop_table('products')
    op.drop_table('configurations')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS qualitylevel')
    op.execute('DROP TYPE IF EXISTS imagetype')
