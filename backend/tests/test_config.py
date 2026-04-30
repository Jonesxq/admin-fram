from app.core.config import Settings
from app.seed import get_initial_admin_password


def test_settings_accepts_seed_environment_variables(tmp_path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join([
            "DATABASE_URL=sqlite+pysqlite:///:memory:",
            "JWT_SECRET_KEY=test-secret",
            "INITIAL_ADMIN_PASSWORD=Admin123!",
            "ALLOW_DEFAULT_ADMIN_PASSWORD=1",
        ]),
        encoding="utf-8",
    )

    settings = Settings(_env_file=env_file)

    assert settings.initial_admin_password == "Admin123!"
    assert settings.allow_default_admin_password is True


def test_seed_initial_admin_password_uses_settings(monkeypatch) -> None:
    settings = Settings(
        database_url="sqlite+pysqlite:///:memory:",
        jwt_secret_key="test-secret",
        initial_admin_password="Admin123!",
        allow_default_admin_password=True,
    )
    monkeypatch.delenv("INITIAL_ADMIN_PASSWORD", raising=False)
    monkeypatch.delenv("ALLOW_DEFAULT_ADMIN_PASSWORD", raising=False)
    monkeypatch.setattr("app.seed.settings", settings, raising=False)

    assert get_initial_admin_password() == "Admin123!"
