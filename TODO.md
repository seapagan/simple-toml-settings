# Future Plans

- Add an Option to look for the config file in the current directory, and if not
  found then look in the users home directory.
- Add an Option to not include the `schema_version` key. By default this key
  **will** be included. **This will only be omited if the `schema_version` is
  'none'**.
- Allow a global config file to be used, which will be overridden by a local
  config file if it exists.
- Add an option to not save config options that have the same value as the
  default.
- By default `save()` should not save config options that are not already in the
  config file, though leave the current behavior as an option.
- Raise a specific custom exception for malformed TOML files

## Possible ideas

These are ideas that I am not totally sure about, but I am considering.

- Allow a custom folder root (not just users $HOME) folder.

## Future Breaking Changes

The following changes are planned for future releases:

- **`strict_get=True` as default**: The `strict_get` parameter currently defaults
  to `False` for backward compatibility. In a future version, this will change to
  `True`, meaning `get()` will raise `KeyError` for missing keys instead of
  returning `None`. Users are encouraged to opt-in to `strict_get=True` now to
  prepare for this change.
