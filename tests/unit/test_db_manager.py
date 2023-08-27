from unittest.mock import call

import pytest
from _pytest.fixtures import FixtureRequest
from pytest_mysqlit.db_manager import DbManager
from callee import Contains


class TestDbManager:

    @pytest.fixture
    def mock_request(self, mocker):
        mock = mocker.patch("_pytest.fixtures", spec=FixtureRequest)
        mock.config.getoption.side_effect = ['test', 'localhost', '3306', 'user', 'password', 'db_name']
        return mock

    @pytest.fixture
    def mock_mysql_connect(self, mocker):
        return mocker.patch("mysql.connector.connect")

    def test__given__request__when__enter_manger__then__setup_correctly(self, mock_request, mock_mysql_connect):
        with DbManager(mock_request):
            mock_mysql_connect.assert_has_calls([call(host='localhost', port='3306', user='user',
                                                         password='password'),
                                                    call(database='db_name', user='user', password='password',
                                                         host='localhost', port='3306')], any_order=True)

            mock_mysql_connect.return_value.cursor.return_value.__enter__.return_value.execute.assert_has_calls(
                [call('DROP DATABASE IF EXISTS db_name;'), call('CREATE DATABASE db_name;')])

    def test__given__request__when__exit_manger__then__teardown_correctly(self, mock_request, mock_mysql_connect):
        with DbManager(mock_request):
            pass

        cursor = mock_mysql_connect.return_value.cursor.return_value.__enter__.return_value.execute
        cursor.assert_any_call(
            Contains('DROP DATABASE IF EXISTS db_name'))

    def test__given__request__when__get_conn__then__return_correct_conn(self, mock_request, mock_mysql_connect):
        with DbManager(mock_request) as sut:
            assert sut.get_conn()
