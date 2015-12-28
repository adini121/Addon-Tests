#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import py
import pytest
import MySQLdb
from time import gmtime, strftime
def pytest_runtest_setup(item):
    pytest_mozwebqa = py.test.config.pluginmanager.getplugin("mozwebqa")
    pytest_mozwebqa.TestSetup.services_base_url = item.config.option.services_base_url


def pytest_addoption(parser):
    parser.addoption("--servicesbaseurl",
                     action="store",
                     dest='services_base_url',
                     metavar='str',
                     default="",
                     help="specify the api url")


def pytest_funcarg__mozwebqa(request):
    pytest_mozwebqa = py.test.config.pluginmanager.getplugin("mozwebqa")
    return pytest_mozwebqa.TestSetup(request)

@pytest.fixture(autouse=True)
def session_id(mozwebqa):
    print 'Session ID: {}'.format(mozwebqa.selenium.session_id)
    str = '{}\n'.format(mozwebqa.selenium.session_id)
    str_session_id = '{}'.format(mozwebqa.selenium.session_id)

    with open ("/home/nisal/python.txt", "a") as myfile:
        myfile.write(str)

    current_time = strftime("%Y-%m-%d %H:%M")
    print('Current time is: {}'.format(current_time))
    """ Connect to MySQL database """
    conn = MySQLdb.connect(host='localhost',
                           user='root',
                           passwd='',
                           db='amo_sessionIDs')
    # if conn.is_connected():
    #         print('Connected to MySQL database')

    c = conn.cursor()
    tblQuery = """CREATE TABLE IF NOT EXISTS test_session_ids (id int unsigned auto_increment not NULL,
        session_id VARCHAR(60) not NULL,
        date_created VARCHAR(100) not NULL,
        primary key(id))"""
    c.execute(tblQuery)
    print('............Successfully created table .......')
    insQuery = """insert into test_session_ids (session_id, date_created) values ('%s', '%s')"""
    # insQuery = """insert into test_session_ids (session_id, date_created) values ('whatever', 'whatever')"""
    c = conn.cursor()
    c.execute("insert into test_session_ids (session_id, date_created) values (%s, %s)", (str_session_id, current_time))
    # c.execute(insQuery)
    print('............Successfully ADDED to table .......')
    # conn.commit()
    conn.close()