"""Test the settings module."""


def test_config_file_auto_created(settings):
    assert settings.settings_folder.exists()
    assert settings.settings_folder.is_dir()
    assert settings.settings_folder.name == "test_app"
    assert settings.settings_file_name == "config.toml"


def test_get_attrs(settings):
    attrs = settings.get_attrs()
    assert attrs["schema_version"] == "none"


def test_get(settings):
    assert settings.get("app_name") == "test_app"
    assert settings.get("nonexistent_key") is None
    assert settings.get("test_string_var") == "test_value"
    assert settings.get("test_int_var") == 42


def test_set(settings):
    settings.set("app_name", "new_test_app")
    assert settings.get("app_name") == "new_test_app"


def test_list_settings(settings):
    settings.set("new_key", "new_value")
    settings_dict = settings.list_settings()
    assert settings_dict["new_key"] == "new_value"


def test_load_settings(settings):
    settings.load()
    # length is 3 because of the 'schema' setting
    assert len(settings.list_settings()) == 3

    assert settings.get("schema_version") == "none"
    assert settings.list_settings()["test_string_var"] == "test_value"
    assert settings.list_settings()["test_int_var"] == 42


def test_set_schema_version(settings):
    settings.set("schema_version", "1.0.0")
    settings.load()
    assert settings.get("schema_version") == "1.0.0"


def test_autosave(settings):
    settings.set("test_string_var", "new_value")
    settings.load()
    assert settings.get("test_string_var") == "new_value"


def test_no_autosave(settings):
    settings.set("test_string_var", "new_value", autosave=False)
    settings.load()
    assert settings.get("test_string_var") == "test_value"
