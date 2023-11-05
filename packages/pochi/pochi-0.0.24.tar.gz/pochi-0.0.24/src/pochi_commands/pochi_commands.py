import argparse
import sys
from logs.manager import LoggingManager
import toml
import os
import configparser
from pathlib import Path
from platformdirs import PlatformDirs


class PochiCommandManager(object):
    def __init__(self, command_providers, subparsers, parser):
        self.__command_providers = command_providers
        self.__subparsers = subparsers
        self.__parser = parser

    def __get_help_text(self):
        help_text = """usage:
    pochi init [--name=<application_package_name>] [--version=<application_version_name>] [--connection=<connection_name] [--distribution={INTERNAL | EXTERNAL}] [--force]
    pochi config [--name=<parameter_name> --value=<parameter_value>]
    pochi [ clean ] [ build ] [ deploy [--application-logic|--application-package] ] [ test [--tests=<testsuite>[.<testname>][,...] ]

Pochi is a CLI tool for building, deploying and testing Snowflake native applications.

Targets:
"""
        return help_text

    def __print_help_text(self):
        print(self.__get_help_text())
        for key in self.__command_providers:
            command = self.__command_providers.get(key)
            print(command.get_help_text())

    def __check_valid_argument(self, action: str, argument: str):
        actions = self.__parser._actions[0].choices
        options = actions[action]._option_string_actions
        found_equal_sign_index = argument.find("=")
        if found_equal_sign_index >= 0:
            argument = argument[:found_equal_sign_index]
        return argument in options

    def __check_list_valid_argument(self, action: str, arguments: [str]):
        for argument in arguments:
            if not self.__check_valid_argument(action, argument):
                return False
        return True

    def __parse_user_command_arguments(self, arguments):
        no_errors = False
        try:
            # Divide argv by commands
            split_argv = [[]]
            for c in arguments:
                if c in self.__subparsers.choices:
                    split_argv.append([c])
                else:
                    split_argv[-1].append(c)
            # Initialize namespace
            args = argparse.Namespace()
            for c in self.__subparsers.choices:
                setattr(args, c, None)
            # Parse each command
            if (
                len(split_argv) > 1
                and len(split_argv[1]) > 0
                and split_argv[1][0] in args
            ):
                self.__parser.parse_args(
                    split_argv[0], namespace=args
                )  # Without command
                for argv in split_argv[1:]:  # Commands
                    n = argparse.Namespace()

                    if self.__check_list_valid_argument(argv[0], argv[1:]):
                        setattr(args, argv[0], n)
                        self.__parser.parse_args(argv, namespace=n)
                    else:
                        no_errors = True

                if not no_errors:
                    setattr(args, "project_config", self.__load_config_files(args))
            else:
                no_errors = True
        except Exception as e:
            LoggingManager.display_single_message(f"Unexpected {type(e)=}: {e=}")
            no_errors = True
        finally:
            if no_errors:
                self.__print_help_text()
                sys.exit()
            return no_errors, args

    def __load_config_files(self, args):
        # Step 1: Process the config/project.toml file
        # If the file does not exist, then this folder is not initialized. Return None
        project_config_file_path = os.path.join("config", "project.toml")

        if os.path.exists(project_config_file_path):
            project_config_data = toml.load(os.path.join("config", "project.toml"))
        else:
            # config/project.toml not found; so there's no app pkg name, no version, no connection name
            return None

        project_config = argparse.Namespace()

        for key, value in project_config_data.items():
            setattr(
                project_config,
                key,
                value,
            )
        # Step 2: Load the Snowflake connections files to look up the project's connection target
        # Snowflake has two types of config files that can be loaded:
        # (1) SnowCLI (https://docs.snowflake.com/LIMITEDACCESS/snowcli/connecting/connect)
        # (2) SnowSQL (https://docs.snowflake.com/en/user-guide/snowsql-config)
        #
        # Pochi searches for connection using the following list of config files:
        # (1) ~/.snowflake/config.toml (if it exists)
        # (2) Snowflake app directory/config.toml (if it exists)
        # (3) ~/.snowsql/config (regular config file, not TOML)
        #
        # There may be other locations but Pochi only supports the above 3 locations at this point.

        # Find SnowCLI config file and use it.
        snowcli_config_toml = os.path.join(os.environ.get("SNOWFLAKE_HOME", os.path.join(Path.home(), ".snowflake")), "config.toml")
        
        if not os.path.exists(snowcli_config_toml):
            snowcli_config_toml = os.path.join(
                PlatformDirs(appname="snowflake", appauthor=False).user_config_path,
                "config.toml"
            )

        snowsql_config = os.path.join(Path.home(), ".snowsql", "config")
        connection_config = None
        connection_config_namespace = None
        if snowcli_config_toml is not None and os.path.exists(snowcli_config_toml):
            # Found the SnowCLI connection toml file; load it!
            connection_config = toml.load(snowcli_config_toml)
            default_connection_config = connection_config.get("connections").get(
                project_config_data.get("default_connection", "Undefined"), None
            )
            connection_config_namespace = argparse.Namespace()
            setattr(
                        connection_config_namespace,
                        "connection_file_path",
                        snowcli_config_toml,
                    )
            if default_connection_config is not None:
                setattr(
                        connection_config_namespace,
                        "is_defined",
                        True,
                )
                for parameter in default_connection_config:
                    setattr(
                        connection_config_namespace,
                        parameter,
                        default_connection_config[parameter],
                    )
            else:
                setattr(
                        connection_config_namespace,
                        "is_defined",
                        False,
                )

        elif os.path.exists(snowsql_config):
            connection_config = configparser.ConfigParser()
            connection_config.read(snowsql_config)

            connection_section_name = "connections." + project_config_data.get(
                "default_connection", "Undefined"
            )
            connection_config_namespace = argparse.Namespace()
            setattr(
                        connection_config_namespace,
                        "connection_file_path",
                        snowsql_config,
                    )
            if connection_config.has_section(connection_section_name):
                setattr(
                        connection_config_namespace,
                        "is_defined",
                        True,
                )
                default_connection_config = connection_config[connection_section_name]
                if ("accountname" in default_connection_config):
                    setattr(
                        connection_config_namespace,
                        "account",
                        default_connection_config["accountname"],
                    )
                if ("username" in default_connection_config):
                    setattr(
                        connection_config_namespace,
                        "user",
                        default_connection_config["username"],
                    )
                if ("password" in default_connection_config):
                    setattr(
                        connection_config_namespace,
                        "password",
                        default_connection_config["password"],
                    )
                if ("rolename" in default_connection_config):
                    setattr(
                        connection_config_namespace,
                        "role",
                        default_connection_config["rolename"],
                    )
                if ("warehousename" in default_connection_config):
                    setattr(
                        connection_config_namespace,
                        "warehouse",
                        default_connection_config["warehousename"],
                    )
                if ("private_key_path" in default_connection_config):
                    setattr(
                        connection_config_namespace,
                        "private_key_path",
                        default_connection_config["private_key_path"],
                    )
            else:
                setattr(
                        connection_config_namespace,
                        "is_defined",
                        False,
                )

        # set default_connection to the connection details, or None if no connection config file found
        setattr(args, "default_connection", connection_config_namespace)
        return project_config

    def execute_commands(self, arguments):
        has_errors, args = self.__parse_user_command_arguments(arguments)
        if args.help != None:
            self.__print_help_text()
            # self.__help_command.execute(args)
            sys.exit(0)

        if args.init != None:
            self.__command_providers.get("init_command").execute(args)
            sys.exit(0)

        if args.config != None:
            self.__command_providers.get("config_command").execute(args)
            sys.exit(0)

        if args.clean != None:
            self.__command_providers.get("clean_command").execute(args)

        if args.build != None:
            self.__command_providers.get("build_command").execute(args)

        if args.deploy != None:
            if args.build == None:
                self.__command_providers.get("build_command").execute(args)
            self.__command_providers.get("deploy_command").execute(args)

        if args.test != None:
            self.__command_providers.get("test_command").execute(args)

        if (
            arguments[0]
            not in [
                "init",
                "config",
                "clean",
                "build",
                "deploy",
                "test",
            ]
            and hasattr(args, arguments[0])
            and getattr(args, arguments[0]) != None
        ):
            self.__command_providers.get(arguments[0]).execute(args)
