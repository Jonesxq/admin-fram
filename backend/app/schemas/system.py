from datetime import datetime

from pydantic import BaseModel


class UserItem(BaseModel):
    id: int
    username: str
    nickname: str
    email: str | None = None
    mobile: str | None = None
    dept_id: int | None = None
    status: str
    last_login_at: datetime | None = None


class RoleItem(BaseModel):
    id: int
    code: str
    name: str
    data_scope: str
    sort: int
    status: str


class MenuItem(BaseModel):
    id: int
    parent_id: int | None = None
    type: str
    title: str
    path: str | None = None
    component: str | None = None
    permission: str | None = None
    icon: str | None = None
    sort: int
    status: str


class DeptItem(BaseModel):
    id: int
    parent_id: int | None = None
    ancestors: str
    name: str
    sort: int
    status: str


class PostItem(BaseModel):
    id: int
    code: str
    name: str
    sort: int
    status: str


class DictTypeItem(BaseModel):
    id: int
    code: str
    name: str
    status: str


class ConfigItem(BaseModel):
    id: int
    key: str
    value: str
    name: str
    remark: str | None = None


class LoginLogItem(BaseModel):
    id: int
    username: str
    success: bool
    message: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    created_at: datetime


class OperationLogItem(BaseModel):
    id: int
    username: str | None = None
    permission: str | None = None
    title: str
    method: str | None = None
    path: str | None = None
    ip_address: str | None = None
    success: bool
    message: str | None = None
    created_at: datetime
