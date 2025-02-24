import random
import sqlite3
import string

import pytest

from core.database_interaction_methods import insert_variables, insert_employers, insert_jobs, \
    insert_documents, insert_document_storage, insert_document_variables


def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters, k=length))


@pytest.fixture
def db_connection():
    conn = sqlite3.connect("../data/applications.sqlite")
    yield conn
    conn.close()


def test_insert_and_verify_employers(db_connection):
    employer_name = random_string()
    industry = random_string()
    location = random_string()
    notes = random_string()
    insert_employers(employer_name, industry, location, notes)
    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT employerID, employer_name, industry, location, notes FROM Employers WHERE employer_name = ? AND industry = ? AND location = ? AND notes = ?",
        (employer_name, industry, location, notes))
    result = cursor.fetchone()
    assert result is not None
    cursor.execute("DELETE FROM Employers WHERE employerID = ?", (result[0],))
    db_connection.commit()


def test_insert_and_verify_jobs(db_connection):
    job_title = random_string()
    employer_id = 1
    location = random_string()
    insert_jobs(job_title, employer_id, location)
    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT jobID, job_title, location FROM Jobs WHERE job_title = ? AND employerID = ? AND location = ?",
        (job_title, employer_id, location))
    result = cursor.fetchone()
    assert result is not None
    cursor.execute("DELETE FROM Jobs WHERE jobID = ?", (result[0],))
    db_connection.commit()


def test_insert_and_verify_documents(db_connection):
    job_id = 1
    document_type = random_string()
    insert_documents(job_id, document_type)
    cursor = db_connection.cursor()
    cursor.execute("SELECT documentID, documentType FROM Documents WHERE jobID = ? AND documentType = ?",
                   (job_id, document_type))
    result = cursor.fetchone()
    assert result is not None
    cursor.execute("DELETE FROM Documents WHERE documentID = ?", (result[0],))
    db_connection.commit()


def test_insert_and_verify_document_storage(db_connection):
    document_id = 1
    file_type = "pdf"
    path = "/some/path/"
    file_name = random_string() + ".pdf"
    insert_document_storage(document_id, file_type, path, file_name)
    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT storageID FROM Document_Storage WHERE documentID = ? AND fileType = ? AND path = ? AND file_name = ?",
        (document_id, file_type, path, file_name))
    result = cursor.fetchone()
    assert result is not None
    cursor.execute("DELETE FROM Document_Storage WHERE storageID = ?", (result[0],))
    db_connection.commit()


def test_insert_and_verify_variables(db_connection):
    variable_name = random_string()
    insert_variables(variable_name)
    cursor = db_connection.cursor()
    cursor.execute("SELECT variableID, variable_name FROM Variables WHERE variable_name = ?", (variable_name,))
    result = cursor.fetchone()
    assert result is not None
    cursor.execute("DELETE FROM Variables WHERE variableID = ?", (result[0],))
    db_connection.commit()


def test_insert_and_verify_document_variables(db_connection):
    document_id, variable_id = 1, 1
    placeholder_name = random_string()
    insert_document_variables(document_id, variable_id, placeholder_name)
    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT documentID, variableID FROM Document_Variables WHERE documentID = ? AND variableID = ? AND placeholder_name = ?",
        (document_id, variable_id, placeholder_name))
    result = cursor.fetchone()
    assert result is not None
    cursor.execute("DELETE FROM Document_Variables WHERE documentID = ? AND variableID = ?", (document_id, variable_id))
    db_connection.commit()
