#!/usr/bin/env python
"""Command-line utility for administrative tasks."""
import argparse
import json
import sys
from pathlib import Path

from scripts import script_classes

BASE_DIR = Path(__file__).resolve().parent.parent


class ScriptRunner:
    """
    This class facilitates the execution of script files through method calls.
    """

    def __init__(self, class_name, args):
        self.class_name = class_name
        self.args = args

    def run(self):
        """
        This method fetches an instance of a script class, sets the input data
        for the script, and then calls the script class's execute method.
        """
        args_vars = json.loads(self.args)
        api = script_classes.get(self.class_name)
        if not api:
            raise ModuleNotFoundError(self.class_name)
        api_object = api()
        if hasattr(api_object, "InputParams"):
            api_object.input = api_object.InputParams(**args_vars)
        api_object.execute()


def set_environment(env: str) -> None:
    """
    This function sets up the environment, loads the corresponding .env file
    for the given environment, and performs necessary imports.
    """
    from dotenv import load_dotenv

    load_dotenv(dotenv_path=f".env.{env}")
    from lms_scripts.config import resources
    from helpers.connection import connection

    connection.set_env(env)


def confirm_production_execution() -> None:
    """
    This function is used to confirm the execution of a file in a production environment
    before proceeding further.
    """
    confirmation = input(
        "Are you sure you want to run this script in production environment? (yes/no): "
    )
    if confirmation.lower() != "yes":
        print("Execution in production environment aborted.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Run this file with environment, script class name and it's arguments."
    )
    parser.add_argument(
        "--env",
        type=str,
        choices=["dev", "stg", "prod"],
        required=True,
        help="Environment to run script on.",
    )
    parser.add_argument("class_name", type=str, help="The name of the class to run.")
    parser.add_argument(
        "--args",
        type=str,
        nargs="?",
        default="{}",
        help="Arguments to pass to the class (optional).",
    )

    input = parser.parse_args()

    if input.env == "prod":
        confirm_production_execution()

    set_environment(input.env)

    script_runner = ScriptRunner(input.class_name, input.args)
    script_runner.run()


if __name__ == "__main__":
    main()
