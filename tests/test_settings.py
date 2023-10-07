def test_get_attrs(settings):
    attrs = settings.get_attrs()
    assert attrs["schema_version"] == "none"


def test_get(settings):
    assert settings.get("app_name") == "test_app"
    assert settings.get("nonexistent_key") is None


def test_set(settings):
    settings.set("app_name", "new_test_app")
    assert settings.get("app_name") == "new_test_app"


def test_list_settings(settings):
    settings.set("new_key", "new_value")
    settings_dict = settings.list_settings()
    assert settings_dict["new_key"] == "new_value"
