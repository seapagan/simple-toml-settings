# Future Plans

- Allow a custom folder root (not just users $HOME) folder.
- Add an Option to look for the config file in the current directory, and if not
  found then look in the users home directory.
- Add an Option to not include the `schema_version` key. By default this key
  **will** be included. **This will only be ommited if the `schema_version` is
  'none'**.
- Allow a global config file to be used, which will be overridden by a local
  config file if it exists.
- Add an option to not save config options that have the same value as the
  default.
- By default `save()` should not save config options that are not already in the
  config file, though leave the current behavior as an option.
- Raise a specific custom exception for malformed TOML files
