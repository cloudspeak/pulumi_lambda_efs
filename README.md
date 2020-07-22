# Pulumi Lambda EFS Dependencies
![Code formatting badge](https://img.shields.io/github/workflow/status/cloudspeak/pulumi-lambda-efs/code_formatting?label=code%20formatting "Code formatting badge")
![Code quality badge](https://img.shields.io/github/workflow/status/cloudspeak/pulumi-lambda-efs/code_quality?label=code%20quality "Code quality badge")
![Coding style badge](https://img.shields.io/github/workflow/status/cloudspeak/pulumi-lambda-efs/coding_style?label=coding%20style "Coding style badge")
![Unit tests badge](https://img.shields.io/github/workflow/status/cloudspeak/pulumi-lambda-efs/unit_tests?label=unit%20tests "Unit tests badge")

This package provides some Pulumi components and shell scripts which support the use of
AWS Lambda functions which get their dependencies from an EFS filesystem.  It supports
two types of dependencies:
* Pip packages listed in a `requirements.txt` file
* Linuxbrew formulae listed in a `Brewfile`.

Before your Lambda can use dependencies from EFS, you must create a
`DevelopmentEnvironment` in your Pulumi script, and configure your Lambdas to use it


# Development

## Getting started

You need Python 3 (preferably 3.8) installed to start working on this project.

In order to install your virtualenv, just go to the root of the project and:
```bash
make install
```

## IDE

Nuage recommends [Visual Studio Code](https://code.visualstudio.com/download) to work on this project, and some default settings have been configured in the [.vscode/settings.json](.vscode/settings.json).

These settings merely enforce the code-quality guidelines defined below, but if you use another IDE it's probably worth taking a quick look at it to ensure compliance with the standard.

By default, we recommend:
1. Putting your virtualenv in a `venv` folder at the project root
2. Using a `.env` file to define your environment variables (cf. [python-dotenv](https://pypi.org/project/python-dotenv/))

## Unit tests

To run the unit tests, use the following command:

```
python setup.py test
```

## Code quality

This project has opinionated code-quality requirements:
- Code formatter: [black](https://black.readthedocs.io/en/stable/)
- Code linter: [pylint](https://www.pylint.org)
- Code style guidelines: [flake8](https://flake8.pycqa.org/en/latest/)

All of these tools are enforced at the commit-level via [pre-commit](https://pre-commit.com)

You can run the following command to apply code-quality to your project at any point:
```bash
make quality
```

Code quality configuration files:
- IDE-agnostic coding style settings are set in the [.editorconfig](.editorconfig) file
- Python-related settings are set in the [setup.cfg](setup.cfg) file
- Pre-commit-related settings are set in the [.pre-commit-config.yaml](.pre-commit-config.yaml) file

## Folder structure

```
.
├── .github/workflow/on_push.yml            The Github Actions workflow
├── example                                 An example program which uses this provider package
│   ├── __main__.py
│   ├── Pulumi.dev.yaml
│   ├── Pulumi.yaml
│   └── README.md
├── Makefile
├── pulumi_lambda_efs                      The main package folder with a subfolder for each resource type
├── README.md
├── requirements_dev.txt
├── setup.cfg
└── setup.py
```
