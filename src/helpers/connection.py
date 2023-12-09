"""
This file contains class for creating and maintaining multiple db creations. 
"""
import os
from configparser import ConfigParser

import psycopg2


class Connection:
    """
    This class is used to create and maintain database
    connections for multiple services.
    """

    def __init__(self, env):
        self.active_connections = {}
        self.env = env

    def __del__(self):
        # When the Connection object is deleted, close all active connections.
        # List cast to solve Runtimeerror: Dictionary Changed Size During Iteration.
        for db_name in list(self.active_connections):
            self.close_connection(db_name)

    def get_connection(self, db_name):
        """
        This method is used to return an active connection if present,
        else create a connection and then return it.
        """
        conn = self.active_connections.get(db_name)
        if not conn:
            params = self.config(db_name)
            print(f"Connecting to the {db_name} PostgreSQL database...")
            conn = psycopg2.connect(**params)

            self.active_connections[db_name] = conn
        return conn

    def get_cursor(self, db_name):
        """
        This method is used to get a database cursor for
        executing SQL queries.
        """
        return self.get_connection(db_name).cursor()

    def close_connection(self, db_name):
        """
        This method is used to close a database connection and
        remove it from the active connections dictionary.
        """
        conn = self.active_connections.pop(db_name, None)
        if conn:
            conn.close()
            print(f"Connection to {db_name} server is closed.")
        else:
            print(f"No active connection found for {db_name}.")

    def config(self, db_name):
        """
        This method is used to get database credentials
        from a database.ini configuration file.
        """
        from execute import BASE_DIR

        filename = os.path.join(BASE_DIR, f"src\\database.{self.env}.ini")

        parser = ConfigParser()
        parser.read(filename)

        if parser.has_section(db_name):
            params = dict(parser.items(db_name))
            return params
        else:
            raise Exception(f"DB name {db_name} not found in the {filename} file.")


class ConnectionManager:
    """
    A class for managing connections and environment settings.
    """

    _conn: Connection = None
    _env: str = None

    def connection(self):
        if not self._conn:
            self._conn = Connection(self._env)
        return self._conn

    def set_env(self, env: str):
        if self._conn:
            del self._conn

        self._env = env
        return self

    def __getattr__(self, name):
        return getattr(self.connection(), name)


connection = ConnectionManager()
