# Rabbit MQ Examples in Python

<p align="left">
    <a href="https://www.rabbitmq.com/">
        <img src="https://img.shields.io/badge/RabbitMQ-FF6600?logo=rabbitmq&logoColor=white&style=flat" alt="RabbitMQ Badge"/>
    </a>
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=flat" alt="Python Badge"/>
    </a>
    <a href="https://wiki.python.org/moin/TkInter">
        <img src="https://img.shields.io/badge/Tkinter-FFB000?logo=python&logoColor=white&style=flat" alt="Tkinter Badge"/>
    </a>
</p>

RabbitMQ is a popular open-source message broker that enables applications to communicate with each other using messages, following the Advanced Message Queuing Protocol (AMQP). It is widely used for building scalable and distributed systems, allowing for reliable message delivery, decoupling of application components, and asynchronous processing. With Python, you can interact with RabbitMQ using libraries such as `pika` to send and receive messages between producers and consumers.

This app illustrates integration of RabbitMQ in Python using the Pika library. 

### Advanced Message Queuing Protocol

AMQP (Advanced Message Queuing Protocol) is an open-standard application layer protocol for message-oriented middleware. It defines a high-level, flexible, and robust way for applications to exchange messages asynchronously, reliably, and securely.

At its core, AMQP is about communication between software components where messages are sent to an intermediary (a message broker like RabbitMQ) rather than directly to recipients. This "store and forward" mechanism decouples senders (producers) from receivers (consumers), enhancing system flexibility, scalability, and resilience

AMQP supports various messaging patterns, including point-to-point, publish/subscribe, and request/reply. Its strength lies in its explicit definitions for features like message acknowledgments, persistent messages, and transaction support, ensuring reliable message delivery even in complex distributed systems. This makes AMQP a foundational protocol for building robust, scalable, and event-driven architectures.

## Ruff integration and linting

Ruff is an incredibly fast Python linter and formatter written in Rust. It aims to replace a multitude of Python code quality tools like Flake8, Black, isort, pydocstyle, and more, all within a single, highly performant tool.

This documentation will cover how to use Ruff from the command line, assuming you have it installed (e.g., via pip install ruff or poetry add --group dev ruff).

### Ruff's core commands 

Ruff primarily offers two main modes of operation: linting (checking for code quality issues) and formatting (ensuring consistent code style).

1.1. ruff check (Linting)

The ruff check command is used to identify and report linting violations in your Python code.

To check all Python files in the current directory and its subdirectories:

```
ruff check .
```

To check specific files and directories

```
ruff check my_module.py another_folder/
```

Example output of ruff 

```
my_module.py:5:1: F841 Local variable `unused_variable` is assigned to but never used
my_module.py:10:8: E701 Multiple statements on one line (colon)
Found 2 errors.
```

Ruff check command examples with arguments

```
ruff check --fix .

ruff check --fix-only .

ruff check --diff .

ruff check --select F401,E701 . # Only check for unused imports (F401) and multiple statements on one line (E701)

ruff check --ignore E501 . # Ignore line too long errors

ruff check --show-source .

ruff check --watch .

ruff clean

ruff check --show-files

ruff check --show-settings path/to/my_file.py
```

1.2. Ruff Formatting

```
ruff format .

ruff format my_module.py another_folder/

```

Format command with options

```
ruff format --check .
```

### Running ruff commands with Poetry 

```
poetry run ruff check .

poetry run ruff check --fix .
```

## Installing and configuring pre-commit hooks 

Create .pre-commit-config.yaml file at the root of your project. Then, install pre-commit

```
poetry run pre-commit install
```

Run pre-commit hooks manually on all the files 

```
poetry run pre-commit run --all-files
```

Install the hooks in git using this command

```
poetry run pre-commit install
```

### Forcing constraints on commit messages

```YAML
repos:
  # Ruff hooks for linting and formatting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.8 # Check for the latest stable release!
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  # Hook for enforcing Conventional Commits
  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v2.4.0 # Check for the latest stable release of this hook!
    hooks:
      - id: conventional-pre-commit
        # This hook runs during the 'commit-msg' stage
        # stages: [commit-msg] # This is the default stage for commit message hooks
        args:
          - feat # Allow 'feat:'
          - fix  # Allow 'fix:'
```

After modifying .pre-commit-config.yaml, you need to update the installed hooks for the changes to take effect:

```
poetry run pre-commit install --hook-type commit-msg
poetry run pre-commit install --hook-type pre-commit # To re-ensure the default pre-commit hook is also installed
```

You can also run poetry run pre-commit install without specifying --hook-type. By default, pre-commit install installs the pre-commit and commit-msg hooks (among others if default_install_hook_types is configured). However, being explicit with --hook-type commit-msg guarantees it.
