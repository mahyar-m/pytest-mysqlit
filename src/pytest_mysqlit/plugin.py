import pytest

from _pytest.fixtures import FixtureRequest
from pytest_mysqlit.db_manager import DbManager

pytest_options = [
    {
        'name': 'mysqlit_global_fixtures_path',
        'option': '--mysqlit-global-fixtures-path',
        'default': 'tests/integration/fixtures/mysql',
        'help': '',
    },
    {
        'name': 'mysql_host',
        'option': '--mysql-host',
        'default': '127.0.0.1',
        'help': '',
    },
    {
        'name': 'mysql_port',
        'option': '--mysql-port',
        'default': 3306,
        'help': '',
    },
    {
        'name': 'mysql_user',
        'option': '--mysql-user',
        'default': 'root',
        'help': '',
    },
    {
        'name': 'mysql_password',
        'option': '--mysql-password',
        'default': 'password',
        'help': '',
    },
    {
        'name': 'mysql_db_name',
        'option': '--mysql-db-name',
        'default': 'test_mysql',
        'help': '',
    },
]


def pytest_addoption(parser) -> None:
    """Configure for pytest-mysqlit"""

    for option in pytest_options:
        parser.addini(
            name=option['name'],
            default=option['default'],
            help=option['help'],
        )

        parser.addoption(
            option['option'],
            action='store',
            dest=option['name'],
        )


@pytest.fixture(scope="session")
def dbm_session_fixture(request: FixtureRequest) -> DbManager:
    with DbManager(request) as db_manager:
        yield db_manager


@pytest.fixture(scope="class")
def dbm_class_fixture(dbm_session_fixture, request: FixtureRequest) -> DbManager:
    dbm_session_fixture.execute_sql_file('setup_class.sql', location='local', request=request)
    yield dbm_session_fixture
    dbm_session_fixture.execute_sql_file('teardown_class.sql', location='local', request=request)


@pytest.fixture(scope="function")
def dbm_function_fixture(dbm_class_fixture, request: FixtureRequest) -> DbManager:
    dbm_class_fixture.execute_sql_file('setup_method.sql', location='local', request=request)
    yield dbm_class_fixture
    dbm_class_fixture.execute_sql_file('teardown_method.sql', location='local', request=request)
