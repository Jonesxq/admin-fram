from app.models.base import Base
from app.models import system


def test_system_tables_are_registered() -> None:
    table_names = set(Base.metadata.tables.keys())

    assert "sys_user" in table_names
    assert "sys_role" in table_names
    assert "sys_menu" in table_names
    assert "sys_dept" in table_names
    assert "sys_post" in table_names
    assert "sys_dict_type" in table_names
    assert "sys_dict_item" in table_names
    assert "sys_config" in table_names
    assert "sys_login_log" in table_names
    assert "sys_operation_log" in table_names
    assert system.User.__tablename__ == "sys_user"
