from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


sys_user_role = Table(
    "sys_user_role",
    Base.metadata,
    Column("user_id", ForeignKey("sys_user.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", ForeignKey("sys_role.id", ondelete="CASCADE"), primary_key=True),
)

sys_role_menu = Table(
    "sys_role_menu",
    Base.metadata,
    Column("role_id", ForeignKey("sys_role.id", ondelete="CASCADE"), primary_key=True),
    Column("menu_id", ForeignKey("sys_menu.id", ondelete="CASCADE"), primary_key=True),
)

sys_user_post = Table(
    "sys_user_post",
    Base.metadata,
    Column("user_id", ForeignKey("sys_user.id", ondelete="CASCADE"), primary_key=True),
    Column("post_id", ForeignKey("sys_post.id", ondelete="CASCADE"), primary_key=True),
)


class User(TimestampMixin, Base):
    __tablename__ = "sys_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    nickname: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str | None] = mapped_column(String(128), nullable=True)
    mobile: Mapped[str | None] = mapped_column(String(32), nullable=True)
    dept_id: Mapped[int | None] = mapped_column(ForeignKey("sys_dept.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="enabled", nullable=False)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    dept: Mapped["Dept | None"] = relationship(back_populates="users")
    roles: Mapped[list["Role"]] = relationship(
        secondary=sys_user_role,
        back_populates="users",
    )
    posts: Mapped[list["Post"]] = relationship(
        secondary=sys_user_post,
        back_populates="users",
    )


class Role(TimestampMixin, Base):
    __tablename__ = "sys_role"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    data_scope: Mapped[str] = mapped_column(String(32), default="all", nullable=False)
    sort: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="enabled", nullable=False)

    users: Mapped[list[User]] = relationship(
        secondary=sys_user_role,
        back_populates="roles",
    )
    menus: Mapped[list["Menu"]] = relationship(
        secondary=sys_role_menu,
        back_populates="roles",
    )


class Menu(TimestampMixin, Base):
    __tablename__ = "sys_menu"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("sys_menu.id"), nullable=True)
    type: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(64), nullable=False)
    path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    component: Mapped[str | None] = mapped_column(String(255), nullable=True)
    permission: Mapped[str | None] = mapped_column(String(128), nullable=True)
    icon: Mapped[str | None] = mapped_column(String(64), nullable=True)
    sort: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="enabled", nullable=False)

    parent: Mapped["Menu | None"] = relationship(remote_side=[id], back_populates="children")
    children: Mapped[list["Menu"]] = relationship(back_populates="parent")
    roles: Mapped[list[Role]] = relationship(
        secondary=sys_role_menu,
        back_populates="menus",
    )


class Dept(TimestampMixin, Base):
    __tablename__ = "sys_dept"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("sys_dept.id"), nullable=True)
    ancestors: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    sort: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="enabled", nullable=False)

    parent: Mapped["Dept | None"] = relationship(remote_side=[id], back_populates="children")
    children: Mapped[list["Dept"]] = relationship(back_populates="parent")
    users: Mapped[list[User]] = relationship(back_populates="dept")


class Post(TimestampMixin, Base):
    __tablename__ = "sys_post"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    sort: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="enabled", nullable=False)

    users: Mapped[list[User]] = relationship(
        secondary=sys_user_post,
        back_populates="posts",
    )


class DictType(TimestampMixin, Base):
    __tablename__ = "sys_dict_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="enabled", nullable=False)

    items: Mapped[list["DictItem"]] = relationship(back_populates="dict_type")


class DictItem(TimestampMixin, Base):
    __tablename__ = "sys_dict_item"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    dict_type_id: Mapped[int] = mapped_column(ForeignKey("sys_dict_type.id"), nullable=False)
    value: Mapped[str] = mapped_column(String(128), nullable=False)
    label: Mapped[str] = mapped_column(String(128), nullable=False)
    sort: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="enabled", nullable=False)

    dict_type: Mapped[DictType] = relationship(back_populates="items")


class Config(TimestampMixin, Base):
    __tablename__ = "sys_config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    remark: Mapped[str | None] = mapped_column(String(255), nullable=True)


class LoginLog(Base):
    __tablename__ = "sys_login_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(64), nullable=False)
    success: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    message: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class OperationLog(Base):
    __tablename__ = "sys_operation_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str | None] = mapped_column(String(64), nullable=True)
    permission: Mapped[str | None] = mapped_column(String(128), nullable=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    method: Mapped[str | None] = mapped_column(String(16), nullable=True)
    path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(64), nullable=True)
    success: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    message: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
