"""Test the settings module."""

from pathlib import Path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from pytest_mock import MockerFixture

from simple_toml_settings.exceptions import (
    SettingsMutuallyExclusiveError,
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

    def test_settings_folder_created_when_already_exists(
        self, fs: FakeFilesystem
    ) -> None:
        """Test that creating settings when folder exists doesn't fail.

        This tests the fix for a TOCTOU race condition where the directory
        could be created by another process between exists() and mkdir().
        """
        fs.create_dir(Path.home())

        # Create the settings folder manually first
        test_folder = Path.home() / ".test_app_race"
        test_folder.mkdir(parents=True, exist_ok=False)

        # Creating a settings instance should not fail even though dir exists
        settings = TOMLSettings("test_app_race")
        assert settings.settings_folder.exists()
        assert settings.settings_folder == test_folder

    def test_exception_raised_on_missing_config_if_auto_create_is_false(
        self, fs: FakeFilesystem
    ) -> None:
        """Test that the settings file is not created if auto_create False."""
        fs.create_dir(Path.home())

        with pytest.raises(SettingsNotFoundError):
            TOMLSettings("test_app", auto_create=False)

    def test_allow_missing_file_disables_auto_create(
        self, fs: FakeFilesystem
    ) -> None:
        """Test that allow_missing_file disables auto_create."""
        fs.create_dir(Path.home())
        settings = CustomSettings(
            "test_app", auto_create=True, allow_missing_file=True
        )
        assert settings.settings_folder.exists()
        assert settings.settings_folder.is_dir()
        assert settings.settings_folder.name == f".{self.TEST_APP_NAME}"
        # assert that the config file is not created
        assert not (settings.settings_folder / self.SETTINGS_FILE_NAME).exists()
        # assert that 'auto_create' is False
        assert not settings.auto_create

    def test_no_exception_raised_on_missing_config_if_allow_no_file_is_true(
        self, fs: FakeFilesystem
    ) -> None:
        """Test the 'allow_missing_file' option.

        If 'allow_missing_file' is True, and 'auto_create' is False, then the
        settings file is not created, and no exception is raised.
        """
        fs.create_dir(Path.home())

        settings = CustomSettings(
            "test_app", auto_create=False, allow_missing_file=True
        )
        assert settings.settings_folder.exists()
        assert settings.settings_folder.is_dir()
        assert settings.settings_folder.name == f".{self.TEST_APP_NAME}"
        # assert that the config file is not created
        assert not (settings.settings_folder / self.SETTINGS_FILE_NAME).exists()

        # make sure we can still get values from the settings object
        assert settings.get("app_name") == "test_app"
        assert settings.get("my_var") is False

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

    def test_settings_from_environment(self, monkeypatch, fs) -> None:
        """Test that the settings file is read from the xdg variable."""
        monkeypatch.setenv("XDG_CONFIG_HOME", "/path/validity/matters/not")

        settings = SettingsExample("test_app", xdg_config=True)
        assert (
            settings.settings_folder
            == Path("/path/validity/matters/not") / "test_app"
        )

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

    def test_missing_app_section_raises_error(self, fs: FakeFilesystem) -> None:
        """Test that missing [app_name] section raises SettingsNotFoundError."""
        # Create a config file with a different section name
        fs.create_file(
            self.SETTINGS_FILE_NAME,
            contents="[other_app]\ntest_var = 'value'\n",
        )

        # Should raise SettingsNotFoundError, not KeyError
        with pytest.raises(
            SettingsNotFoundError,
            match=r"Config file missing required \[test_app\] section",
        ):
            TOMLSettings("test_app", local_file=True, auto_create=False)

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

    def test_get_instance_with_different_app_names(
        self, fs: FakeFilesystem
    ) -> None:
        """Test that different app_names return different instances.

        This is a regression test for a bug where get_instance() only keyed
        by class, not by app_name, causing different app names to return
        the same instance.
        """
        fs.create_dir(Path.home())
        instance1 = TOMLSettings.get_instance("app1")
        instance2 = TOMLSettings.get_instance("app2")

        # Different app names should return different instances
        assert instance1 is not instance2
        # Each instance should have the correct app_name
        assert instance1.app_name == "app1"
        assert instance2.app_name == "app2"

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

    def test_mutually_exclusive_attributes(self, fs: FakeFilesystem) -> None:
        """Test that mutually exclusive attributes are handled."""
        fs.create_dir(Path.home())

        error_pattern = (
            r"Only one of (flat_config|local_file), "
            r"(flat_config|local_file) can be True\."
        )

        with pytest.raises(SettingsMutuallyExclusiveError, match=error_pattern):
            CustomSettings("test_app", local_file=True, flat_config=True)
