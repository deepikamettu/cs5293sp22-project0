import sys
sys.path.append('..')
import sqlite3
import pytest
from project0 import project0


def testFetchincidentsCaseChecking():
    resultSet = project0.fetchincidents(
        "https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-13_daily_incident_summary.pdf")
    assert True


def testExtractIncidentsCaseChecking():
    incident_data = project0.fetchincidents(
        " https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-13_daily_incident_summary.pdf")
    resultSet = project0.extractincidents(incident_data)
    assert True


def testCreateDBCaseChecking():
    resultSet = project0.createdb()
    assert resultSet == 'normanpd.db'


def testPopulateDBCaseChecking():
    sql = sqlite3.connect('normanpd.db')
    cur = sql.cursor()
    cur.execute('''SELECT * FROM incidents ''')
    resultSet = cur.fetchall()
    assert resultSet is not None


def testStatusCaseChecking():
    resultSet = project0.status('normanpd.db')
    assert True
