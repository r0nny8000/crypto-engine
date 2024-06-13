CRYP2-BOT
=========

This is a simple bot for trading crypto currencies on different exchanges and defi protocols.
 
Getting started
--------------- 

To use the bot, you need to have Python 3.12 or higher installed on your system. You can download Python from the official website: https://www.python.org/downloads/ or use pyenv like described below in the log.

Skip the poetry initialization if you already have a `pyproject.toml` file in your project. Just run the `poetry install` command to install the dependencies.


Log
---

Intalled the latest version of python 3.12.3 on my system with pyenv and set it as the local version.

```bash
$ pyenv install 3.12.3
$ pyenv local 3.12.3
$ python --version
Python 3.12.3
```

Initialized poetry and intalled the dependecies. 

```bash
$ poetry init
$ mkdir cryp2bot
$ touch cryp2bot/cryp2bot.py
$ touch cryp2bot/__init__.py
$ poetry install
$ poerry shell
$ which python
```

Set the python interpreter in VSCode to the version installed with poetry by using CMD+Shift+P and "Select Interpreter".

It seems that this config file is not needed in .vscode/settings.json. The interpreter is selected automatically... sometimes.

    {
        "python.defaultInterpreterPath": "/Users/me/Library/Caches/pypoetry/virtualenvs/cryp2bot-????????-py3.12/bin/python"
    }


Created the first test for the bot.

```bash
$ mkdir tests
$ touch tests/test_cryp2bot.py
$ poetry add --group dev pytest
$ poetry shell
$ pytest
```







