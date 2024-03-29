# Command Line Script Runner

This Python script serves as a command-line utility for administrative tasks. It provides a flexible way to execute various script classes with specified arguments. The script is designed to be used in different environments (dev, stg, prod) and facilitates the execution of scripts through method calls.

## Usage

```bash
python script_runner.py --env <environment> <class_name> [--args <arguments>]
```

### Options

- `--env`: Specifies the environment in which the script should run. Choose from `dev`, `stg`, or `prod`.
- `class_name`: The name of the script class to run.
- `--args`: Optional argument to pass parameters to the script class. Should be a JSON-formatted string.

## Example

```bash
python script_runner.py --env prod MyScriptClass --args '{"param1": "value1", "param2": "value2"}'
```

## Environment Setup

Before running the script, you need to set up the environment using the `set_environment` function. It loads the corresponding `.env` file for the specified environment and performs necessary imports.

```python
set_environment("dev")
```

## Production Execution Confirmation

When attempting to run a script in a production environment (`--env prod`), the script will prompt for confirmation to ensure intentional execution in a production setting.

```bash
Are you sure you want to run this script in the production environment? (yes/no):
```

## Script Classes

The script utilizes script classes for execution. Ensure that the desired script class is available and correctly specified when running the script.

## Dependencies

- [argparse](https://docs.python.org/3/library/argparse.html)
- [json](https://docs.python.org/3/library/json.html)
- [pathlib](https://docs.python.org/3/library/pathlib.html)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

Make sure to install the required dependencies before running the script:

```bash
pip install -r requirements.txt
```

Feel free to adapt and extend this script according to your project's specific needs.
