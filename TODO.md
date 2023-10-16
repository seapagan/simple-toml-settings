# Future Plans

- Allow a custom folder root (not just users $HOME) folder, as well as custom
  file name. Perhaps option to just store the config file in the users home
  directory? The default option of putting it in a sub-folder of the project is
  useful for projects that need to store extra data, but may be overkill for
  basic projects.
- Add Option to look for the config file in the current directory, and if not found
  then look in the users home directory. This would allow for a project to
  override the users config file.
- Add option to disable auto-creating the config file if it doesn't exist.
- Add an Option to not include the `schema_version` key. By default this key
  **will** be included.
