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


class UserCreate(BaseModel):
    username: str
    password: str
    nickname: str
    email: str | None = None
    mobile: str | None = None
    dept_id: int | None = None
    status: str = "enabled"


class UserUpdate(BaseModel):
    nickname: str | None = None
    email: str | None = None
    mobile: str | None = None
    dept_id: int | None = None
    status: str | None = None


class RoleItem(BaseModel):
    id: int
    code: str
    name: str
    data_scope: str
    sort: int
    status: str


class RoleCreate(BaseModel):
    code: str
    name: str
    data_scope: str = "all"
    sort: int = 0
    status: str = "enabled"


class RoleUpdate(BaseModel):
    code: str | None = None
    name: str | None = None
    data_scope: str | None = None
    sort: int | None = None
    status: str | None = None


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


class MenuCreate(BaseModel):
    type: str
    title: str
    parent_id: int | None = None
    path: str | None = None
    component: str | None = None
    permission: str | None = None
    icon: str | None = None
    sort: int = 0
    status: str = "enabled"


class MenuUpdate(BaseModel):
    type: str | None = None
    title: str | None = None
    parent_id: int | None = None
    path: str | None = None
    component: str | None = None
    permission: str | None = None
    icon: str | None = None
    sort: int | None = None
    status: str | None = None


class DeptItem(BaseModel):
    id: int
    parent_id: int | None = None
    ancestors: str
    name: str
    sort: int
    status: str


class DeptCreate(BaseModel):
    name: str
    parent_id: int | None = None
    ancestors: str = ""
    sort: int = 0
    status: str = "enabled"


class DeptUpdate(BaseModel):
    name: str | None = None
    parent_id: int | None = None
    ancestors: str | None = None
    sort: int | None = None
    status: str | None = None


class PostItem(BaseModel):
    id: int
    code: str
    name: str
    sort: int
    status: str


class PostCreate(BaseModel):
    code: str
    name: str
    sort: int = 0
    status: str = "enabled"


class PostUpdate(BaseModel):
    code: str | None = None
    name: str | None = None
    sort: int | None = None
    status: str | None = None


class DictTypeItem(BaseModel):
    id: int
    code: str
    name: str
    status: str


class DictTypeCreate(BaseModel):
    code: str
    name: str
    status: str = "enabled"


class DictTypeUpdate(BaseModel):
    code: str | None = None
    name: str | None = None
    status: str | None = None


class DictItemItem(BaseModel):
    id: int
    dict_type_id: int
    value: str
    label: str
    sort: int
    status: str


class DictItemCreate(BaseModel):
    dict_type_id: int
    value: str
    label: str
    sort: int = 0
    status: str = "enabled"


class DictItemUpdate(BaseModel):
    dict_type_id: int | None = None
    value: str | None = None
    label: str | None = None
    sort: int | None = None
    status: str | None = None


class ConfigItem(BaseModel):
    id: int
    key: str
    name: str
    remark: str | None = None


class ConfigCreate(BaseModel):
    key: str
    value: str
    name: str
    remark: str | None = None


class ConfigUpdate(BaseModel):
    key: str | None = None
    value: str | None = None
    name: str | None = None
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
