"""
This file contains base class for scripts.
"""
from typing import Dict, List, Optional, Tuple, Union

from helpers.connection import Connection, connection
from helpers.strict_dataclass import strict_dataclass


class BaseScript:
    """
    This class is base class for script classes.
    """

    connection: Connection = connection
    input: Optional[strict_dataclass]

    def execute_sql(
        self, sql: str, db_name: str, params: Optional[Union[Dict, List]] = None
    ) -> List[Tuple]:
        """
        This method is used to make db connection and execute the sql.
        """
        cur = self.connection.get_cursor(db_name=db_name)
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)

        return cur.fetchall()

    def execute(self):
        """
        This method is used to manage script call.
        """
        pass
