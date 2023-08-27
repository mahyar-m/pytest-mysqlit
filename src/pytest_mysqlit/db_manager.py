import os
import mysql

from _pytest.fixtures import FixtureRequest
from mysql import connector
from pytest_mysqlit.db_helper import DbHelper
from typing import Self


class DbManager:
    """Class to manage the creation of the test database and handle the connection"""

    def __init__(self, request: FixtureRequest) -> None:
        """Initialize the class."""

        self.request = request
        self.conn = None
        self._internal_conn = None

        self.user = None
        self.password = None
        self.host = None
        self.port = None
        self.db_name = None
        self.global_fixtures_path = None

    def get_conn(self) -> connector.connection:
        """Return a connection"""

        return self.conn

    def get_connection_string(self) -> str:
        """Return connection string"""

        return 'mysql://{user}@{host}:{port}/{db_name}'.format(user=self.user, host=self.host, port=self.port,
                                                               db_name=self.db_name)

    def get_config(self) -> dict:
        """Return config as a dict"""

        return {
            'dbname': self.db_name,
            'user': self.user,
            'password': self.password,
            'host': self.host,
            'port': int(self.port),
        }

    def execute_sql_file(
            self,
            sql_file_path: str,
            location: str = 'local',
            request: FixtureRequest = None,
            local_path: str = None,
            global_path: str = None
    ) -> None:
        """Execute a sql file"""

        if not global_path:
            global_path = os.path.join(self.global_fixtures_path)

        if location == 'local':
            if not local_path:
                local_path = os.path.join(request.fspath.dirname, 'fixtures', 'mysql')
            sql_file_path = os.path.join(local_path, sql_file_path)
        elif location == 'global':
            sql_file_path = os.path.join(global_path, sql_file_path)
        elif location == 'relative':
            pass

        if not os.path.isfile(sql_file_path):
            raise ValueError('{} sql file does not exist'.format(sql_file_path))

        DbHelper.exec_sql_file(self.get_conn(), sql_file_path, global_path)

    def _init_config(self) -> None:
        """Initialize the config from pytest options"""

        for option in ['global_fixtures_path']:
            option_name = 'mysqlit_' + option
            setattr(self, option, self.request.config.getoption(option_name) or self.request.config.getini(option_name))

        for option in ['host', 'port', 'user', 'password', 'db_name']:
            option_name = 'mysql_' + option
            setattr(self, option, self.request.config.getoption(option_name) or self.request.config.getini(option_name))

    def _setup(self) -> None:
        """Setup the test database"""

        self._init_config()

        self._internal_conn = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
        )

        with self._internal_conn.cursor() as cur:
            cur.execute('DROP DATABASE IF EXISTS {};'.format(self.db_name))
            cur.execute('CREATE DATABASE {};'.format(self.db_name))

        self.conn = mysql.connector.connect(
            database=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )

    def _teardown(self) -> None:
        """Teardown the test database"""

        with self._internal_conn.cursor() as cur:
            cur.execute('DROP DATABASE IF EXISTS {}'.format(self.db_name))

    def __enter__(self) -> Self:
        self._setup()
        return self

    def __exit__(self, *exc_details) -> None:
        self._teardown()
        self.conn.close()
