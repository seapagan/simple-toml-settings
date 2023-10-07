# Simple TOML Settings <!-- omit in toc -->

[![Tests](https://github.com/seapagan/simple-toml-settings/actions/workflows/tests.yml/badge.svg)](https://github.com/seapagan/simple-toml-settings/actions/workflows/tests.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/b8793a3d6eb04167b9e2b13e11f1f12d)](https://app.codacy.com/gh/seapagan/simple-toml-settings/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![CodeQL](https://github.com/seapagan/simple-toml-settings/actions/workflows/codeql.yml/badge.svg)](https://github.com/seapagan/simple-toml-settings/actions/workflows/codeql.yml)

A Python library to save your settings in a TOML file.

- [Usage](#usage)
- [Development setup](#development-setup)
  - [Task Runner](#task-runner)
  - [Linting](#linting)
  - [Pre-commit](#pre-commit)
- [License](#license)
- [Credits](#credits)

## Usage

This is a library to save your settings in a TOML file.  It is designed to be
simple to use and to be able to save and load settings from a TOML file.

At the moment there is no functionality, I am just setting up the project and
migrating over the code from within another project that is using this functionality.

## Development setup

Install the dependencies using Poetry:

```console
$ poetry install
```

Then, activate the virtual environment:

```console
$ poetry shell
```

Now, you can start to develop the app.

### Task Runner

The task-runner [Poe the Poet](https://github.com/nat-n/poethepoet) is installed
as a development dependency which allows us to run simple tasks (similar to npm
`scripts`).

These are run (from within the virtual environment) using the `poe` command and
then the script name, for example:

```console
$ poe pre
```

You can define your own, but there are 7 specific ones provided with the script.

- `pre` : Run `pre-commit run --all-files`
- `pylint`: Run Pylint on all Python files in the project.
- `mypy` = Run MyPy type-checker on all Python files in the project.
- `flake8` = Run Flake8 linter on all Python files in the project.
- `black` = Run Black code formatter on all Python files in the project.
- `try` = Run Tryceratops linter on all Python files in the project.

- `lint` = Runs pylint, mypy, flake8 and black in sequence

These are defined in the `pyproject.toml` file in the `[tool.poe.tasks]`
section. Take a look at this file if you want to add or remove tasks.

### Linting

This project includes [flake8](https://flake8.pycqa.org/en/latest/) (with
several plugins) for linting and
[Black](https://black.readthedocs.io/en/stable/) for formatting.
[Mypy](http://mypy-lang.org/) is installed for type checking.
[isort](https://pycqa.github.io/isort/),[Pylint](https://pylint.org/) and
[tyrceratops](https://github.com/guilatrova/tryceratops) are also installed as
standard.

### Pre-commit

There is a [pre-commit](https://pre-commit.com/) configuration provided to run
some checks on the code before it is committed.  This is a great tool to help
keep your code clean.

To install pre-commit, run the following command from inside your venv:

```console
$ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

## License

This project is released under the terms of the MIT license.

## Credits

The original Python boilerplate for this package was created using
[Pymaker](https://github.com/seapagan/py-maker) by [Grant
Ramsay (seapagan)](https://github.com/seapagan)
