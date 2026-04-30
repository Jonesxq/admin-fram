"""initial system tables

Revision ID: 0001_initial_system_tables
Revises:
Create Date: 2026-05-01 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001_initial_system_tables"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def timestamp_columns() -> list[sa.Column]:
    return [
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
    ]


def upgrade() -> None:
    op.create_table(
        "sys_dept",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("ancestors", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("sort", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["parent_id"], ["sys_dept.id"]),
        *timestamp_columns(),
    )
    op.create_table(
        "sys_role",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("data_scope", sa.String(length=32), nullable=False),
        sa.Column("sort", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        *timestamp_columns(),
    )
    op.create_table(
        "sys_menu",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("type", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=64), nullable=False),
        sa.Column("path", sa.String(length=255), nullable=True),
        sa.Column("component", sa.String(length=255), nullable=True),
        sa.Column("permission", sa.String(length=128), nullable=True),
        sa.Column("icon", sa.String(length=64), nullable=True),
        sa.Column("sort", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["parent_id"], ["sys_menu.id"]),
        *timestamp_columns(),
    )
    op.create_table(
        "sys_post",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("sort", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        *timestamp_columns(),
    )
    op.create_table(
        "sys_dict_type",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        *timestamp_columns(),
    )
    op.create_table(
        "sys_config",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("key", sa.String(length=128), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("remark", sa.String(length=255), nullable=True),
        *timestamp_columns(),
    )
    op.create_table(
        "sys_user",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("nickname", sa.String(length=64), nullable=False),
        sa.Column("email", sa.String(length=128), nullable=True),
        sa.Column("mobile", sa.String(length=32), nullable=True),
        sa.Column("dept_id", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("last_login_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["dept_id"], ["sys_dept.id"]),
        *timestamp_columns(),
    )
    op.create_table(
        "sys_dict_item",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("dict_type_id", sa.Integer(), nullable=False),
        sa.Column("value", sa.String(length=128), nullable=False),
        sa.Column("label", sa.String(length=128), nullable=False),
        sa.Column("sort", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["dict_type_id"], ["sys_dict_type.id"]),
        *timestamp_columns(),
    )
    op.create_table(
        "sys_login_log",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("success", sa.Boolean(), nullable=False),
        sa.Column("message", sa.String(length=255), nullable=True),
        sa.Column("ip_address", sa.String(length=64), nullable=True),
        sa.Column("user_agent", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "sys_operation_log",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("username", sa.String(length=64), nullable=True),
        sa.Column("permission", sa.String(length=128), nullable=True),
        sa.Column("title", sa.String(length=128), nullable=False),
        sa.Column("method", sa.String(length=16), nullable=True),
        sa.Column("path", sa.String(length=255), nullable=True),
        sa.Column("ip_address", sa.String(length=64), nullable=True),
        sa.Column("success", sa.Boolean(), nullable=False),
        sa.Column("message", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "sys_user_role",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["sys_role.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["sys_user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "role_id"),
    )
    op.create_table(
        "sys_role_menu",
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("menu_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["menu_id"], ["sys_menu.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["sys_role.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("role_id", "menu_id"),
    )
    op.create_table(
        "sys_user_post",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["post_id"], ["sys_post.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["sys_user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "post_id"),
    )

    op.create_index("ix_sys_user_username", "sys_user", ["username"], unique=True)
    op.create_index("ix_sys_role_code", "sys_role", ["code"], unique=True)
    op.create_index("ix_sys_post_code", "sys_post", ["code"], unique=True)
    op.create_index("ix_sys_dict_type_code", "sys_dict_type", ["code"], unique=True)
    op.create_index("ix_sys_config_key", "sys_config", ["key"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_sys_config_key", table_name="sys_config")
    op.drop_index("ix_sys_dict_type_code", table_name="sys_dict_type")
    op.drop_index("ix_sys_post_code", table_name="sys_post")
    op.drop_index("ix_sys_role_code", table_name="sys_role")
    op.drop_index("ix_sys_user_username", table_name="sys_user")
    op.drop_table("sys_user_post")
    op.drop_table("sys_role_menu")
    op.drop_table("sys_user_role")
    op.drop_table("sys_operation_log")
    op.drop_table("sys_login_log")
    op.drop_table("sys_dict_item")
    op.drop_table("sys_user")
    op.drop_table("sys_config")
    op.drop_table("sys_dict_type")
    op.drop_table("sys_post")
    op.drop_table("sys_menu")
    op.drop_table("sys_role")
    op.drop_table("sys_dept")
