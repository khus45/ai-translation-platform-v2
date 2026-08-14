"""Add intelligence platform tables

Revision ID: 4a1b2c3d4e5f
Revises: 2f6a7b8c9d10
Create Date: 2026-08-14 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "4a1b2c3d4e5f"
down_revision: Union[str, Sequence[str], None] = "2f6a7b8c9d10"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "translations",
        sa.Column(
            "domain", sa.String(length=50), nullable=False, server_default="general"
        ),
    )
    op.add_column(
        "translations",
        sa.Column(
            "prompt_version",
            sa.String(length=50),
            nullable=False,
            server_default="translate-v1",
        ),
    )
    op.add_column(
        "translations",
        sa.Column("latency_ms", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "translations",
        sa.Column("token_cost", sa.Float(), nullable=False, server_default="0"),
    )
    op.add_column(
        "translations",
        sa.Column(
            "retrieved_context",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'[]'::json"),
        ),
    )
    op.create_index(op.f("ix_translations_domain"), "translations", ["domain"])

    op.add_column("feedback", sa.Column("user_id", sa.Integer(), nullable=True))
    op.add_column(
        "feedback",
        sa.Column(
            "status", sa.String(length=30), nullable=False, server_default="pending"
        ),
    )
    op.add_column("feedback", sa.Column("approved", sa.Boolean(), nullable=True))
    op.add_column("feedback", sa.Column("edited_text", sa.Text(), nullable=True))
    op.create_index(op.f("ix_feedback_user_id"), "feedback", ["user_id"])

    op.create_table(
        "documents",
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column(
            "content_type",
            sa.String(length=100),
            nullable=False,
            server_default="text/plain",
        ),
        sa.Column("extracted_text", sa.Text(), nullable=False),
        sa.Column(
            "language",
            sa.String(length=20),
            nullable=False,
            server_default="unknown",
        ),
        sa.Column(
            "domain", sa.String(length=50), nullable=False, server_default="general"
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_documents_id"), "documents", ["id"])
    op.create_index(op.f("ix_documents_user_id"), "documents", ["user_id"])

    op.create_table(
        "glossary_terms",
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("term", sa.String(length=255), nullable=False),
        sa.Column("approved_translation", sa.String(length=255), nullable=False),
        sa.Column(
            "source_language", sa.String(length=20), nullable=False, server_default="en"
        ),
        sa.Column(
            "target_language", sa.String(length=20), nullable=False, server_default="hi"
        ),
        sa.Column(
            "domain", sa.String(length=50), nullable=False, server_default="general"
        ),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_glossary_terms_domain"), "glossary_terms", ["domain"])
    op.create_index(op.f("ix_glossary_terms_id"), "glossary_terms", ["id"])
    op.create_index(op.f("ix_glossary_terms_term"), "glossary_terms", ["term"])
    op.create_index(op.f("ix_glossary_terms_user_id"), "glossary_terms", ["user_id"])

    op.create_table(
        "translation_memory",
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("source_text", sa.Text(), nullable=False),
        sa.Column("translated_text", sa.Text(), nullable=False),
        sa.Column("source_language", sa.String(length=20), nullable=False),
        sa.Column("target_language", sa.String(length=20), nullable=False),
        sa.Column(
            "domain", sa.String(length=50), nullable=False, server_default="general"
        ),
        sa.Column("quality_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("usage_count", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_translation_memory_domain"), "translation_memory", ["domain"]
    )
    op.create_index(op.f("ix_translation_memory_id"), "translation_memory", ["id"])
    op.create_index(
        op.f("ix_translation_memory_user_id"), "translation_memory", ["user_id"]
    )

    op.create_table(
        "quality_reports",
        sa.Column("translation_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("source_text", sa.Text(), nullable=False),
        sa.Column("translated_text", sa.Text(), nullable=False),
        sa.Column("source_language", sa.String(length=20), nullable=False),
        sa.Column("target_language", sa.String(length=20), nullable=False),
        sa.Column(
            "domain", sa.String(length=50), nullable=False, server_default="general"
        ),
        sa.Column("grammar_score", sa.Float(), nullable=False),
        sa.Column("meaning_score", sa.Float(), nullable=False),
        sa.Column("terminology_score", sa.Float(), nullable=False),
        sa.Column("fluency_score", sa.Float(), nullable=False),
        sa.Column("hallucination_score", sa.Float(), nullable=False),
        sa.Column("overall_score", sa.Float(), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column(
            "suggestions",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'[]'::json"),
        ),
        sa.Column(
            "errors", sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")
        ),
        sa.Column(
            "metrics", sa.JSON(), nullable=False, server_default=sa.text("'{}'::json")
        ),
        sa.Column(
            "retrieved_context",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'[]'::json"),
        ),
        sa.Column(
            "prompt_version",
            sa.String(length=50),
            nullable=False,
            server_default="qa-v1",
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["translation_id"], ["translations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_quality_reports_id"), "quality_reports", ["id"])
    op.create_index(
        op.f("ix_quality_reports_translation_id"),
        "quality_reports",
        ["translation_id"],
    )
    op.create_index(op.f("ix_quality_reports_user_id"), "quality_reports", ["user_id"])


def downgrade() -> None:
    op.drop_index(op.f("ix_quality_reports_user_id"), table_name="quality_reports")
    op.drop_index(
        op.f("ix_quality_reports_translation_id"), table_name="quality_reports"
    )
    op.drop_index(op.f("ix_quality_reports_id"), table_name="quality_reports")
    op.drop_table("quality_reports")
    op.drop_index(
        op.f("ix_translation_memory_user_id"), table_name="translation_memory"
    )
    op.drop_index(op.f("ix_translation_memory_id"), table_name="translation_memory")
    op.drop_index(op.f("ix_translation_memory_domain"), table_name="translation_memory")
    op.drop_table("translation_memory")
    op.drop_index(op.f("ix_glossary_terms_user_id"), table_name="glossary_terms")
    op.drop_index(op.f("ix_glossary_terms_term"), table_name="glossary_terms")
    op.drop_index(op.f("ix_glossary_terms_id"), table_name="glossary_terms")
    op.drop_index(op.f("ix_glossary_terms_domain"), table_name="glossary_terms")
    op.drop_table("glossary_terms")
    op.drop_index(op.f("ix_documents_user_id"), table_name="documents")
    op.drop_index(op.f("ix_documents_id"), table_name="documents")
    op.drop_table("documents")
    op.drop_index(op.f("ix_feedback_user_id"), table_name="feedback")
    op.drop_column("feedback", "edited_text")
    op.drop_column("feedback", "approved")
    op.drop_column("feedback", "status")
    op.drop_column("feedback", "user_id")
    op.drop_index(op.f("ix_translations_domain"), table_name="translations")
    op.drop_column("translations", "retrieved_context")
    op.drop_column("translations", "token_cost")
    op.drop_column("translations", "latency_ms")
    op.drop_column("translations", "prompt_version")
    op.drop_column("translations", "domain")
