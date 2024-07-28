"""Test the settings module."""

import os
from pathlib import Path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from pytest_mock import MockerFixture

from simple_toml_settings.exceptions import (
    SettingsNotFoundError,
    SettingsSchemaError,
)
from simple_toml_settings.settings import TOMLSettings
from simple_toml_settings.xdg_config import xdg_config_home

from .conftest import SettingsExample


class CustomSettings(TOMLSettings):
    """Skeleton Class for testing."""

    my_var: bool = False

    def __post_create_hook__(self) -> None:
        """Override the post create hook."""


class TestSettings:
    """Contains tests for the settings module."""

    TEST_APP_NAME = "test_app"
    SETTINGS_FILE_NAME = "config.toml"
    SETTINGS_FILE_CONTENT = """
[test_app]
test_string_var = 'local_app'
schema_version= '1'
"""

    def test_config_file_auto_created(self, settings: SettingsExample) -> None:
        """Test that the settings file is created if it doesn't exist."""
        assert settings.settings_folder.exists()
        assert settings.settings_folder.is_dir()
        assert settings.settings_folder.name == f".{self.TEST_APP_NAME}"
        assert settings.settings_file_name == self.SETTINGS_FILE_NAME

    def test_exception_raised_on_missing_config_if_auto_create_is_false(
        self, fs: FakeFilesystem
    ) -> None:
        """Test that the settings file is not created if auto_create False."""
        fs.create_dir(Path.home())

        with pytest.raises(SettingsNotFoundError):
            TOMLSettings("test_app", auto_create=False)

    def test_local_config(self, fs: FakeFilesystem) -> None:
        """Test that local_config loads settings from the local directory."""
        fs.create_file(
            self.SETTINGS_FILE_NAME,
            contents=self.SETTINGS_FILE_CONTENT,
        )
        settings = TOMLSettings("test_app", local_file=True, schema_version="1")
        assert settings.get("app_name") == "test_app"
        assert settings.get("test_string_var") == "local_app"

    def test_flat_config(self, flat_settings: SettingsExample) -> None:
        """Test that flat_config loads settings from home folder directly."""
        assert flat_settings.get("app_name") == "test_app"
        assert flat_settings.get("test_string_var") == "test_value"

        assert flat_settings.settings_folder == Path.home()
        assert Path(Path.home() / self.SETTINGS_FILE_NAME).exists()

    def test_xdg_config(self, xdg_settings: SettingsExample) -> None:
        """Test that settings file is created in the xdg_config_home folder."""
        assert xdg_settings.settings_folder.exists()
        assert xdg_settings.settings_folder.is_dir()
        assert xdg_settings.settings_folder.name == f"{self.TEST_APP_NAME}"
        assert xdg_settings.settings_file_name == self.SETTINGS_FILE_NAME
        assert (
            xdg_settings.settings_folder
            == xdg_config_home() / f"{self.TEST_APP_NAME}"
        )

        assert xdg_settings.get("app_name") == "test_app"
        assert xdg_settings.get("test_string_var") == "test_value"

    def test_settings_from_environment(self) -> None:
        """Test that the settings file is loaded from the xdg variable."""
        xdg_orig_value = os.environ.get("XDG_CONFIG_HOME", None)
        home_path = Path.home()
        expected_path = home_path / ".config"
        default_path = xdg_config_home()
        assert default_path == expected_path

        expected_path = home_path / "/path/validity/matters/not"
        assert os.environ.get("XDG_CONFIG_HOME_ALT") == str(expected_path)

        # alternate path does not exist
        os.environ.setdefault(
            "XDG_CONFIG_HOME", os.environ["XDG_CONFIG_HOME_ALT"]
        )
        modified_xdg_path = xdg_config_home()
        assert modified_xdg_path != expected_path
        assert modified_xdg_path == default_path

        # alternate path does exist
        os.environ.setdefault("XDG_CONFIG_HOME", str(home_path))
        assert modified_xdg_path == xdg_config_home()

        # reset to pre-test env value
        if xdg_orig_value:
            os.environ.setdefault("XDG_CONFIG_HOME", xdg_orig_value)

    def test_post_create_hook_is_called(
        self, fs: FakeFilesystem, mocker: MockerFixture
    ) -> None:
        """Test that the post_create_hook is called after file created."""
        fs.create_dir(Path.home())

        mocker.patch.object(TOMLSettings, "__post_create_hook__")
        settings = TOMLSettings("test_app")

        assert settings.__post_create_hook__.called

    def test_post_create_hook_is_called_for_custom_class(
        self, fs: FakeFilesystem, mocker
    ) -> None:
        """Test that the post_create_hook is called after file created."""
        fs.create_dir(Path.home())

        mocker.patch.object(CustomSettings, "__post_create_hook__")
        settings = CustomSettings("test_app")

        assert settings.__post_create_hook__.called

    def test_get_attrs(self, settings) -> None:
        """Test that we can get the attributes of the settings object."""
        attrs = settings.get_attrs()
        assert attrs["schema_version"] == "none"
        assert attrs["test_string_var"] == SettingsExample.test_string_var
        assert attrs["test_int_var"] == SettingsExample.test_int_var

    def test_get_attrs_ignores_none_by_default(self, settings) -> None:
        """Test that None attributes are not returned."""
        settings.set("new_key", None)
        attrs = settings.get_attrs()
        assert "new_key" not in attrs

    def test_save_ignores_none_values(self, settings) -> None:
        """Test that None attributes are not saved."""
        settings.set("new_key", None)
        settings.save()
        attrs = settings.get_attrs()
        assert "new_key" not in attrs

    def test_get_attrs_returns_none_if_include_none_true(
        self, settings
    ) -> None:
        """Test that None attributes are returned if required is True."""
        settings.set("new_key", None)
        attrs = settings.get_attrs(include_none=True)
        assert attrs["new_key"] is None

    def test_get(self, settings) -> None:
        """Test we can get settings."""
        assert settings.get("app_name") == self.TEST_APP_NAME
        assert (
            settings.get("test_string_var") == SettingsExample.test_string_var
        )
        assert settings.get("test_int_var") == SettingsExample.test_int_var

    def test_get_missing_setting(self, settings: SettingsExample) -> None:
        """Test that 'None' is returned when a setting is missing."""
        assert settings.get("missing_setting") is None

    def test_set(self, settings: SettingsExample) -> None:
        """Test that a setting can be set."""
        settings.set("app_name", "new_test_app")
        assert settings.get("app_name") == "new_test_app"

    def test_add_and_list_setting(self, settings: SettingsExample) -> None:
        """Add a new setting and list all settings."""
        settings.set("new_key", "new_value")
        settings_dict = settings.list_settings()
        assert settings_dict["new_key"] == "new_value"

    def test_add_none_value(self, settings: SettingsExample) -> None:
        """Test that a setting can be set to None."""
        settings.set("new_key", None)
        assert settings.get("new_key") is None

    def test_load_settings(self, settings: SettingsExample) -> None:
        """Test that settings are loaded from the settings file."""
        settings.load()
        # length is 3 because of the 'schema' setting
        assert len(settings.list_settings()) == 3  # noqa: PLR2004

        assert settings.get("schema_version") == "none"
        assert settings.list_settings()["test_string_var"] == "test_value"
        assert (
            settings.list_settings()["test_int_var"]
            == SettingsExample.test_int_var
        )

    def test_set_schema_version(self, settings: SettingsExample) -> None:
        """Test that the schema_version can be set using the 'set' method."""
        settings.set("schema_version", "1.0.0")
        settings.load()
        assert settings.get("schema_version") == "1.0.0"

    def test_autosave(self, settings: SettingsExample) -> None:
        """Test that settings are auto saved when autosave is True."""
        settings.set("test_string_var", "new_value")
        settings.load()
        assert settings.get("test_string_var") == "new_value"

    def test_no_autosave(self, settings: SettingsExample) -> None:
        """Test that settings are not auto saved when autosave is False."""
        settings.set("test_string_var", "new_value", autosave=False)
        settings.load()
        assert settings.get("test_string_var") == "test_value"

    def test_custom_file_name(self, fs: FakeFilesystem) -> None:
        """Test that the settings file name can be customized."""
        custom_file_name = "custom_config.toml"

        fs.create_dir(Path.home())
        settings = TOMLSettings("test_app", settings_file_name=custom_file_name)

        assert (Path.home() / ".test_app" / custom_file_name).exists()

        assert settings.settings_file_name == custom_file_name
        assert settings.settings_folder.name == f".{self.TEST_APP_NAME}"
        assert settings.settings_folder / settings.settings_file_name

    def test_items_on_ignored_attrs(self, settings: SettingsExample) -> None:
        """Test that the ignored attributes are not returned by items()."""
        list_settings = settings.list_settings()

        for setting in settings._ignored_attrs:  # noqa: SLF001
            assert setting not in list_settings

    def test_schema_version_mismatch_raises_error(
        self, fs: FakeFilesystem
    ) -> None:
        """Test that a schema version mismatch raises SettingsSchemaError."""
        fs.create_file(
            self.SETTINGS_FILE_NAME,
            contents=self.SETTINGS_FILE_CONTENT,
        )
        with pytest.raises(SettingsSchemaError):
            TOMLSettings("test_app", local_file=True, schema_version="2")

    @pytest.mark.parametrize("value", ["none", "NONE", "None"])
    def test_none_schema_does_not_raise_error(
        self, fs: FakeFilesystem, value: str
    ) -> None:
        """Test that a 'none' schema does NOT raise SettingsSchemaError."""
        fs.create_file(
            self.SETTINGS_FILE_NAME,
            contents="[test_app]\ntest_var = 'schema test'\n"
            f"schema_version='{value}'",
        )

        # this should NOT raise an exception
        TOMLSettings("test_app", local_file=True, schema_version="2")

    def test_missing_schema_does_not_raise_error(
        self, fs: FakeFilesystem
    ) -> None:
        """Test that a 'none' schema does NOT raise SettingsSchemaError."""
        fs.create_file(
            self.SETTINGS_FILE_NAME,
            contents="[test_app]\ntest_var = 'schema test'\n",
        )

        # this should NOT raise an exception
        TOMLSettings("test_app", local_file=True, schema_version="2")

    def test_get_instance(self, fs: FakeFilesystem) -> None:
        """Test that we can get the instance of the settings object."""
        fs.create_dir(Path.home())
        assert isinstance(TOMLSettings.get_instance("test_app"), TOMLSettings)

    def test_get_instance_is_singleton(self, fs: FakeFilesystem) -> None:
        """Test that the instance is a singleton."""
        fs.create_dir(Path.home())
        instance1 = TOMLSettings.get_instance("test_app")
        instance2 = TOMLSettings.get_instance("test_app")
        assert instance1 is instance2

    def test_get_instance_with_custom_class_is_singleton(
        self, fs: FakeFilesystem
    ) -> None:
        """Test that the instance is a singleton."""
        fs.create_dir(Path.home())
        instance1 = CustomSettings.get_instance("test_app")
        instance2 = CustomSettings.get_instance("test_app")
        assert instance1 is instance2

    def test_get_instance_with_multiple_subclasses_not_equal(
        self, fs: FakeFilesystem
    ) -> None:
        """Test that two subclasses are different instances."""
        fs.create_dir(Path.home())
        instance1 = CustomSettings.get_instance("test_app")
        instance2 = SettingsExample.get_instance("test_app")

        assert instance1 is not instance2  # type: ignore[comparison-overlap]

    def test_get_instance_with_custom_class(self, fs: FakeFilesystem) -> None:
        """Test that we can get the instance of a custom settings class."""
        fs.create_dir(Path.home())
        assert isinstance(
            CustomSettings.get_instance("test_app"), CustomSettings
        )

    def test_get_instance_attribute(self, fs: FakeFilesystem) -> None:
        """Test that we can get the instance of the settings object."""
        fs.create_dir(Path.home())
        settings = CustomSettings.get_instance("test_app")
        assert settings.my_var is False
