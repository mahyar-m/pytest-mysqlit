import pytest


@pytest.fixture
def pytester_fixture(pytester):
    def pytester_setup(params):
        pytester.makeconftest(
            """
            pytest_plugins = [
                "src.pytest_mysqlit.plugin",
            ]        
            """
        )

        pytester.makepyfile(
            f"""
            def test__given__fixture__when__testing__then__correct_config(dbm_session_fixture):
                assert dbm_session_fixture.get_config() == {{'dbname': '{params['db_name']}', 'host': '{params['host']}',
                 'password': '{params['password']}', 'port': {params['port']}, 'user': '{params['user']}'}}
                assert dbm_session_fixture.global_fixtures_path == '{params['global_fixtures_path']}'
            """
        )

        return pytester

    return pytester_setup


def test__given__default_input__when__init__then__correct_config(pytester_fixture):
    pytester = pytester_fixture(
        {'db_name': 'test_mysql', 'host': '127.0.0.1', 'password': 'password', 'port': '3306', 'user': 'root',
         'global_fixtures_path': 'tests/integration/fixtures/mysql'})

    result = pytester.runpytest()

    result.assert_outcomes(passed=1)


def test__given__ini_input__when__init__then__correct_config(pytester_fixture):
    pytester = pytester_fixture(
        {'db_name': 'test_db', 'host': 'test_host', 'password': 'test_password', 'port': '12345', 'user': 'test_user',
         'global_fixtures_path': 'test_fixture_path'})

    pytester.makefile(".ini", pytest="""
    [pytest]
    mysql_host=test_host
    mysql_port=12345
    mysql_user=test_user
    mysql_password=test_password
    mysql_db_name=test_db
    mysqlit_global_fixtures_path=test_fixture_path
    """)

    result = pytester.runpytest()

    result.assert_outcomes(passed=1)


def test__given__cli_input__when__init__then__correct_config(pytester_fixture):
    pytester = pytester_fixture(
        {'db_name': 'test_db', 'host': 'test_host', 'password': 'test_password', 'port': '12345', 'user': 'test_user',
         'global_fixtures_path': 'test_fixture_path'})

    result = pytester.runpytest("--mysql-host", "test_host", "--mysql-port", "12345",
                                "--mysql-user", "test_user", "--mysql-password", "test_password",
                                "--mysql-db-name", "test_db", "--mysqlit-global-fixtures-path",
                                "test_fixture_path")

    result.assert_outcomes(passed=1)
