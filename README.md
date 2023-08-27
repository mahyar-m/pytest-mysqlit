# pytest-mysqlit

[![PyPI version][]][1]

[![Python versions][]][1]

[![See Build Status on Travis CI][]][2]

[![See Build Status on AppVeyor][]][3]

MySQL Integration Test in Python

## Features

-   Easy integration test
-   Session/Class/Function level fixtures

## Installation

You can install "pytest-mysqlit" via [pip][] from [PyPI][]:

    $ pip install pytest-mysqlit

## Setup

This pluging uses pytest.ini or the option that passes to the pytest
to configure the connection to database and also find the path to 
the global fixtures.

A sample pytest.ini:
```
testpaths =
    tests/integration
mysql_host=127.0.0.1
mysql_port=3306
mysql_user=root
mysql_password=password
mysql_db_name=test_integration
mysqlit_global_fixtures_path=tests/integration/fixtures/mysql
```
Or command line option:
```
--mysql-host 127.0.0.1
...
```

## Run tests
```
python3 -m venv venv
source venv/bin/activate
pip install -r test-requirements.txt
docker-compose down -v;docker-compose up
python -m pytest tests/integration
```

Run unit test:
```
python -m pytest tests/unit
```

## Usage

This plugin contains different fixtures to help setup and 
teardown the MySQL database. Each of these will put 
the database in a proper state for the test function.

- dbm_session_fixture:
- dbm_class_fixture:
- dbm_function_fixture:


## Contributing

Contributions are very welcome. Tests can be run with [tox][], please
ensure the coverage at least stays the same before you submit a pull
request.

## License

Distributed under the terms of the [MIT][] license, "pytest-mysqlit" is
free and open source software

## Issues

If you encounter any problems, please [file an issue][] along with a
detailed description.

  [PyPI version]: https://img.shields.io/pypi/v/pytest-mysqlit.svg
  [1]: https://pypi.org/project/pytest-mysqlit
  [Python versions]: https://img.shields.io/pypi/pyversions/pytest-mysqlit.svg
  [See Build Status on Travis CI]: https://travis-ci.org/mahyar-m/pytest-mysqlit.svg?branch=master
  [2]: https://travis-ci.org/mahyar-m/pytest-mysqlit
  [See Build Status on AppVeyor]: https://ci.appveyor.com/api/projects/status/github/mahyar-m/pytest-mysqlit?branch=master
  [3]: https://ci.appveyor.com/project/mahyar-m/pytest-mysqlit/branch/master
  [pytest]: https://github.com/pytest-dev/pytest
  [Cookiecutter]: https://github.com/audreyr/cookiecutter
  [@hackebrot]: https://github.com/hackebrot
  [cookiecutter-pytest-plugin]: https://github.com/pytest-dev/cookiecutter-pytest-plugin
  [pip]: https://pypi.org/project/pip/
  [PyPI]: https://pypi.org/project
  [tox]: https://tox.readthedocs.io/en/latest/
  [MIT]: http://opensource.org/licenses/MIT
  [file an issue]: https://github.com/mahyar-m/pytest-mysqlit/issues