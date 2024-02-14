"""Test the settings module."""
from pathlib import Path

import pytest

from simple_toml_settings.exceptions import (
    SettingsNotFoundError,
    SettingsSchemaError,
)
from simple_toml_settings.settings import TOMLSettings

from .conftest import SettingsExample

TEST_APP_NAME = "test_app"


def test_config_file_auto_created(settings) -> None:
    """Test that the settings file is created if it doesn't exist."""
    assert settings.settings_folder.exists()
    assert settings.settings_folder.is_dir()
    assert settings.settings_folder.name == f".{TEST_APP_NAME}"
    assert settings.settings_file_name == "config.toml"


def test_exception_raised_on_missing_config_if_auto_create_is_false(fs) -> None:
    """Test that the settings file is not created if auto_create is False."""
    fs.create_dir(Path.home())

    with pytest.raises(SettingsNotFoundError):
        TOMLSettings("test_app", auto_create=False)


def test_local_config(fs) -> None:
    """Test that local_config loads settings from the local directory."""
    fs.create_file(
        "config.toml",
        contents="[test_app]\ntest_string_var = 'local_app'\nschema_version=1",
    )
    settings = TOMLSettings("test_app", local_file=True, schema_version="1")
    assert settings.get("app_name") == "test_app"
    assert settings.get("test_string_var") == "local_app"


def test_post_create_hook_is_called(fs, mocker) -> None:
    """Test that the post_create_hook is called after settings file created."""
    fs.create_dir(Path.home())

    mocker.patch.object(TOMLSettings, "__post_create_hook__")
    settings = TOMLSettings("test_app")

    assert settings.__post_create_hook__.called


def test_get_attrs(settings) -> None:
    """Test that we can get the attributes of the settings object."""
    attrs = settings.get_attrs()
    assert attrs["schema_version"] == "none"
    assert attrs["test_string_var"] == SettingsExample.test_string_var
    assert attrs["test_int_var"] == SettingsExample.test_int_var


def test_get_attrs_ignores_none_by_default(settings) -> None:
    """Test that None attributes are not returned."""
    settings.set("new_key", None)
    attrs = settings.get_attrs()
    assert "new_key" not in attrs


def test_save_ignores_none_values(settings) -> None:
    """Test that None attributes are not saved."""
    settings.set("new_key", None)
    settings.save()
    attrs = settings.get_attrs()
    assert "new_key" not in attrs


def test_get_attrs_returns_none_if_include_none_true(settings) -> None:
    """Test that None attributes are returned if required is True."""
    settings.set("new_key", None)
    attrs = settings.get_attrs(include_none=True)
    assert attrs["new_key"] is None


def test_get(settings) -> None:
    """Test we can get settings."""
    assert settings.get("app_name") == TEST_APP_NAME
    assert settings.get("test_string_var") == SettingsExample.test_string_var
    assert settings.get("test_int_var") == SettingsExample.test_int_var


def test_get_missing_setting(settings) -> None:
    """Test that 'None' is returned when a setting is missing."""
    assert settings.get("missing_setting") is None


def test_set(settings) -> None:
    """Test that a setting can be set."""
    settings.set("app_name", "new_test_app")
    assert settings.get("app_name") == "new_test_app"


def test_add_and_list_setting(settings) -> None:
    """Add a new setting and list all settings."""
    settings.set("new_key", "new_value")
    settings_dict = settings.list_settings()
    assert settings_dict["new_key"] == "new_value"


def test_add_none_value(settings) -> None:
    """Test that a setting can be set to None."""
    settings.set("new_key", None)
    assert settings.get("new_key") is None


def test_load_settings(settings) -> None:
    """Test that settings are loaded from the settings file."""
    settings.load()
    # length is 3 because of the 'schema' setting
    assert len(settings.list_settings()) == 3  # noqa: PLR2004

    assert settings.get("schema_version") == "none"
    assert settings.list_settings()["test_string_var"] == "test_value"
    assert (
        settings.list_settings()["test_int_var"] == SettingsExample.test_int_var
    )


def test_set_schema_version(settings) -> None:
    """Test that the schema_version can be set using the 'set' method."""
    settings.set("schema_version", "1.0.0")
    settings.load()
    assert settings.get("schema_version") == "1.0.0"


def test_autosave(settings) -> None:
    """Test that settings are auto saved when autosave is True."""
    settings.set("test_string_var", "new_value")
    settings.load()
    assert settings.get("test_string_var") == "new_value"


def test_no_autosave(settings) -> None:
    """Test that settings are not auto saved when autosave is False."""
    settings.set("test_string_var", "new_value", autosave=False)
    settings.load()
    assert settings.get("test_string_var") == "test_value"


def test_custom_file_name(fs) -> None:
    """Test that the settings file name can be customized."""
    custom_file_name = "custom_config.toml"

    fs.create_dir(Path.home())
    settings = TOMLSettings("test_app", settings_file_name=custom_file_name)

    assert (Path.home() / ".test_app" / custom_file_name).exists()

    assert settings.settings_file_name == custom_file_name
    assert settings.settings_folder.name == f".{TEST_APP_NAME}"
    assert settings.settings_folder / settings.settings_file_name


def test_items_on_ignored_attrs(settings) -> None:
    """Test that the ignored attributes are not returned by items()."""
    list_settings = settings.list_settings()

    for setting in settings._ignored_attrs:  # noqa: SLF001
        assert setting not in list_settings


def test_schema_version_mismatch_raises_error(fs) -> None:
    """Test that a schema version mismatch raises SettingsSchemaError."""
    fs.create_file(
        "config.toml",
        contents="[test_app]\ntest_string_var = 'local_app'\nschema_version=1",
    )
    with pytest.raises(SettingsSchemaError):
        TOMLSettings("test_app", local_file=True, schema_version="2")


@pytest.mark.parametrize("value", ["none", "NONE", "None"])
def test_none_schema_does_not_raise_error(fs, value) -> None:
    """Test that a 'none' schema does NOT raise SettingsSchemaError."""
    fs.create_file(
        "config.toml",
        contents="[test_app]\ntest_var = 'schema test'\n"
        f"schema_version='{value}'",
    )

    # this should NOT raise an exception
    TOMLSettings("test_app", local_file=True, schema_version="2")


def test_missing_schema_does_not_raise_error(fs) -> None:
    """Test that a 'none' schema does NOT raise SettingsSchemaError."""
    fs.create_file(
        "config.toml", contents="[test_app]\ntest_var = 'schema test'\n"
    )

    # this should NOT raise an exception
    TOMLSettings("test_app", local_file=True, schema_version="2")
