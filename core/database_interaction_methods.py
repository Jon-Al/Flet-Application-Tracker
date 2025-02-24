import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any, Union

from core.global_handlers import UNIVERSAL_DATABASE_HANDLER as UDH


# region <generic methods>


def select(table_or_view: str, columns: Optional[Dict[str, str] | List[str] | str] = None,
           where: Optional[str] = None,
           params: Optional[tuple] = None,
           limit: int = 10,
           offset: int = 0
           ):
    """
    :param table_or_view: Name of the table or view to select.
    :param columns: List or dict with column names as keys and aliases as values.
    :param where: Conditions.
    :param params: Query parameters.
    :param limit: Maximum number of rows to return.
    :param offset: Offset.
    :return: List of lists or list of dictionaries (depending on the current mode). Each sub-structure represents a single row.
    """
    q_parts = ["SELECT"]
    if not columns:
        q_parts.append("*")
    elif isinstance(columns, str):
        if columns.strip().lower() in {'', 'all', '*'}:
            q_parts.append("*")
        else:
            q_parts.append(columns)
    elif isinstance(columns, List):
        col_strings = ', '.join(filter(None, columns))
        q_parts.append(col_strings)
    elif isinstance(columns, Dict):
        col_strings = []
        for column_name, column_display_name in columns.items():
            if not column_name:
                continue
            elif not column_display_name:
                col_strings.append(column_name)
            else:
                if "'" in column_display_name:
                    col_strings.append(f'{column_name} AS "{column_display_name}"')
                else:
                    col_strings.append(f"{column_name} AS '{column_display_name}'")
        col_strings = ', '.join(filter(None, col_strings))
        q_parts.append(col_strings)
    q_parts.append(f'FROM {table_or_view}')
    if where:
        q_parts.append(where)
    if limit and limit >= 0:
        q_parts.append(f"LIMIT {limit}")
        if offset:
            q_parts.append(f"OFFSET {offset}")
    query_text = " ".join(q_parts)
    return UDH.execute_query(query_text, params, fetchall=-1)


def _insert_(q, p) -> int:
    try:
        r = UDH.execute_query(q, p, -1)
        return max(r, -1)
    except sqlite3.IntegrityError:
        return -1


def _select_(q: str, p=(), f=-1):
    UDH.execute_mode('row')
    return UDH.execute_query(q, p, f)


def update(table: str, pk_column: str, pk_value: Any, updates: Dict[str, Any]) -> bool:
    """
    Updates a record in the SQLite database. Requires a primary key for the update.
    :param table: Name of the table to update.
    :param pk_column: The primary key column name.
    :param pk_value: The primary key value.
    :param updates: A dictionary of column-value pairs to update.
    :return: True if a row was updated, False otherwise.
    """
    if not updates:
        raise ValueError("No updates provided.")

    set_clause = ", ".join(f"{col} = ?" for col in updates.keys())
    p = list(updates.values()) + [pk_value]
    q = f"""
        UPDATE {table}
        SET {set_clause}
        WHERE {pk_column} = ?
    """
    return UDH.execute_query(q, p, fetchall=-1)


def delete(table: str, pk_columns: List[str], pk_values: List[int]) -> int:
    """
    Deletes a record from the SQLite database based on the primary key.
    :param table: Name of the table to delete from.
    :param pk_columns: The primary key(s) column name.
    :param pk_values: The primary key(s) value.
    :return: True if a row was deleted, False otherwise.
    """
    if len(pk_columns) != len(pk_values):
        return -1

    q = f"""
        DELETE FROM {table}
        WHERE {' AND '.join(f"{pk} = ?" for pk in pk_columns)}  
    """
    return UDH.execute_query(q, tuple(pk_values, ), fetchall=-1)


# endregion method
# region <insert  methods>

def insert_employers(employer_name: str,
                     industry: Optional[str] = None,
                     location: Optional[str] = None,
                     notes: Optional[str] = None
                     ) -> int:
    """
    Insert a new employer and return status and ID.
    Returns rowid or -1.
    """
    q = 'INSERT INTO Employers (employer_name, industry, location, notes) VALUES (?, ?, ?, ?)'
    p = (employer_name, industry, location, notes)
    return _insert_(q, p)


def insert_jobs(job_title: str,
                employer_id: int,
                location: str = 'Toronto, ON',
                url: str = '',
                status: str = 'applied',
                annual_pay: Optional[int] = None,
                ft_pt: str = 'Full Time',
                job_type: str = 'Permanent',
                work_model: str = 'In Person',
                date_added: datetime = datetime.now(),
                date_applied: Optional[datetime] = None,
                job_text: str = '',
                notes: str = '',
                archived: bool = False
                ) -> int:
    """
    Insert a new job and return status and ID.
    Returns (success, job_id) where success is a boolean and job_id is the ID if successful.
    """
    q = """
        INSERT INTO Jobs (job_title, employerID, location, URL, status, annual_pay, ft_pt, job_type, work_model, 
                         date_added, date_applied, job_text, notes, archived)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    p = (job_title, employer_id, location, url, status, annual_pay or 0, ft_pt, job_type, work_model,
         date_added, date_applied, job_text, notes, archived)
    return _insert_(q, p)


def insert_documents(job_id: int, document_type: str) -> int:
    """
    Insert a new document and return status and ID.
    Returns (success, document_id) where success is a boolean and document_id is the ID if successful.
    """
    q = """
                INSERT INTO Documents (jobID, documentType)
                VALUES (?, ?)"""
    p = (job_id, document_type)
    return _insert_(q, p)


def insert_document_storage(document_id: int, file_type: str, path: str, file_name: str) -> int:
    """
    Insert a new document storage entry and return success status.
    """
    q = """
    INSERT INTO Document_Storage (documentID, fileType, path, file_name)
    VALUES (?, ?, ?, ?)"""
    p = (document_id, file_type, path, file_name)
    return _insert_(q, p)


def insert_variables(variable_name: str) -> int:
    """
    Insert a new variable and return status and ID.
    Returns (success, variable_id) where success is a boolean and variable_id is the ID if successful.
    """
    q = """
    INSERT INTO Variables (variable_name)
    VALUES (?)"""
    p = (variable_name,)
    return _insert_(q, p)


def insert_document_variables(document_id: int, variable_id: int, placeholder_name: Optional[str] = None) -> int:
    """
    Insert a new document variable relationship and return success status.
    """
    q = """
    INSERT INTO Document_Variables (documentID, variableID, placeholder_name)
    VALUES (?, ?, ?)"""
    p = (document_id, variable_id, placeholder_name)
    return _insert_(q, p)


# endregion insert methods
# region <select all methods>
def select_all_employers():
    q = """SELECT * FROM Employers"""
    return _select_(q)


def select_all_jobs():
    q = """SELECT * FROM Jobs"""
    return _select_(q)


def select_all_document_storage():
    q = """SELECT * FROM Document_Storage"""
    return _select_(q)


def select_all_document_variables():
    q = """SELECT * FROM Document_Variables"""
    return _select_(q)


def select_all_documents():
    q = """SELECT * FROM Documents"""
    return _select_(q)


def select_all_variables():
    q = """SELECT * FROM Variables"""
    return _select_(q)


# endregion <select all> methods
# region <select by methods>
def select_employer(employer_id: int):
    """
    Select an employer by ID.
    Returns the employer as a dictionary or None if not found.
    """
    q = """
    SELECT employerID, employer_name, industry, location, notes
    FROM Employers
    WHERE employerID = ?
    """
    return _select_(q, (employer_id,))


# endregion delete methods

def select_job(job_id: int) -> Optional[Dict[str, Any]]:
    """
    Select a job by ID.
    Returns the job as a dictionary or None if not found.
    """
    q = """
    SELECT j.jobID, j.job_title, j.employerID, e.employer_name, j.location, j.URL, 
           j.status, j.annual_pay, j.ft_pt, j.job_type, j.work_model, 
           j.date_added, j.date_applied, j.job_text, j.notes, j.archived
    FROM Jobs j
    JOIN Employers e ON j.employerID = e.employerID
    WHERE j.jobID = ?
    """
    return _select_(q, (job_id,))


def select_jobs_by_employer(employer: Union[int, str]):
    """
    Select all jobs for a specific employer.
    """
    if isinstance(employer, int):
        q = """SELECT * 
        FROM Jobs  
        WHERE  employerID = ?
        """
    else:
        q = """SELECT * 
        FROM Jobs  
        WHERE employerID IN (
        SELECT employerID FROM Employers WHERE employer_name = ?
        )"""
    return _select_(q, (employer,))


# DOCUMENT OPERATIONS

def select_document(document_id: int) -> Optional[Dict[str, Any]]:
    """
    Select a document by ID.
    Returns the document as a dictionary or None if not found.
    """
    q = """
    SELECT d.documentID, d.jobID, d.documentType
    FROM Documents d
    WHERE d.documentID = ?
    """
    return _select_(q, (document_id,), -1)


def select_documents_by_job(job_id: int) -> List[Dict[str, Any]]:
    """
    Select all documents for a specific job.
    """
    q = """
        SELECT d.documentID, d.documentType, ds.fileType, ds.file_name
        FROM Documents d
        LEFT JOIN Document_Storage ds ON d.documentID = ds.documentID
        WHERE d.jobID = ?
        ORDER BY d.documentType
        """
    return _select_(q, (job_id,), -1)


def select_document_storage(document_id: int) -> Optional[Dict[str, Any]]:
    """
    Select document storage information by document ID.
    """
    q = """
        SELECT ds.documentID, ds.fileType, ds.path, ds.file_name
        FROM Document_Storage ds
        WHERE ds.documentID = ?
        """
    return _select_(q, (document_id,), -1)


def search_employers(employer_id: Optional[int] = None,
                     employer_name: Optional[str] = None,
                     industry: Optional[str] = None,
                     location: Optional[str] = None,
                     notes: Optional[str] = None,
                     last_updated: Optional[datetime] = None,
                     limit: Optional[int] = None,
                     offset: Optional[int] = None):
    """
    Search for employers by name, industry or location.
    """
    if not any([employer_id, employer_name, industry, location, notes, last_updated]):
        return []
    cols = {'employer_id':   employer_id,
            'employer_name': employer_name,
            'industry':      industry,
            'location':      location,
            'notes':         notes,
            'last_updated':  last_updated}

    where = []
    p = []
    for k, v in cols.items():
        if v:
            where.append(f'{k} =?')
            p.append(v)
    q = f"""
          SELECT *
          FROM Employers
          WHERE {' AND '.join(where)}
          ORDER BY employer_name 
          """
    if limit:
        q += f""" LIMIT {limit}"""
        if offset:
            q += f""" OFFSET {offset}"""
    return _select_(q, p, -1)


# endregion <select by methods>
# region update methods

def update_employer(employer_id: int, employer_name: Optional[str] = None,
                    industry: Optional[str] = None, location: Optional[str] = None,
                    notes: Optional[str] = None) -> int:
    """
    Update employer information.
    Only provided parameters will be updated.
    """

    # Get current data first
    current = select_employer(employer_id)
    if not current:
        return False
    employer_name = employer_name if employer_name is not None else current['employer_name']
    industry = industry if industry is not None else current['industry']
    location = location if location is not None else current['location']
    notes = notes if notes is not None else current['notes']
    q = """UPDATE Employers SET employer_name = ?, industry = ?, location = ?, notes = ?
    WHERE employerID = ?"""
    return UDH.execute_query(q, (employer_id, employer_name, industry, location, notes, employer_id), -1)


def update_job(job_id: int, job_title: Optional[str] = None, location: Optional[str] = None,
               url: Optional[str] = None, status: Optional[str] = None,
               annual_pay: Optional[int] = None, ft_pt: Optional[str] = None,
               job_type: Optional[str] = None, work_model: Optional[str] = None,
               date_applied: Optional[datetime] = None, job_text: Optional[str] = None,
               notes: Optional[str] = None, archived: Optional[bool] = None) -> int:
    """
    Update job information.
    Only provided parameters will be updated.
    """
    # Get current data first
    current = select_job(job_id)
    if not current:
        return False
    # Use current values if new ones not provided
    job_title = job_title if job_title is not None else current['job_title']
    location = location if location is not None else current['location']
    url = url if url is not None else current['url']
    status = status if status is not None else current['status']
    annual_pay = annual_pay if annual_pay is not None else current['annual_pay']
    ft_pt = ft_pt if ft_pt is not None else current['ft_pt']
    job_type = job_type if job_type is not None else current['job_type']
    work_model = work_model if work_model is not None else current['work_model']
    date_applied = date_applied if date_applied is not None else current['date_applied']
    job_text = job_text if job_text is not None else current['job_text']
    notes = notes if notes is not None else current['notes']
    archived = archived if archived is not None else current['archived']
    update_query = """
    UPDATE Jobs
    SET job_title = ?, location = ?, URL = ?, status = ?, 
        annual_pay = ?, ft_pt = ?, job_type = ?, work_model = ?,
        date_applied = ?, job_text = ?, notes = ?, archived = ?
    WHERE jobID = ?
    """
    return UDH.execute_query(update_query, (
        job_title, location, url, status,
        annual_pay, ft_pt, job_type, work_model,
        date_applied, job_text, notes, archived,
        job_id
    ), -1)


# endregion update methods

# region <delete methods>
def delete_variables(variable_id: int) -> bool:
    """
    Delete a variables by primary-key(s).
    """
    q = "DELETE FROM Variables WHERE variableID = ?"
    return UDH.execute_query(q, (variable_id,))


def delete_employers(employer_id: int) -> bool:
    """
    Deletes an employers by primary-key(s).
    """
    q = "DELETE FROM Employers WHERE employerID = ?"
    return UDH.execute_query(q, (employer_id,))


def delete_documents(document_id: int) -> bool:
    """
    Delete a documents by primary-key(s).
    """
    q = "DELETE FROM Documents WHERE documentID = ?"
    return UDH.execute_query(q, (document_id,))


def delete_document_storage(storage_id: int) -> bool:
    """
    Delete a document storage by primary-key(s).
    """
    q = "DELETE FROM Document_Storage WHERE storageID = ?"
    return UDH.execute_query(q, (storage_id,))


def delete_jobs(job_id: int) -> bool:
    """
    Delete a jobs by primary-key(s).
    """
    q = "DELETE FROM Jobs WHERE jobID = ?"
    return UDH.execute_query(q, (job_id,))


def delete_document_variables(document_id: int, variable_id: int) -> bool:
    """
    Delete a document variables by primary-key(s).
    """
    q = "DELETE FROM Document_Variables WHERE documentID = ? AND variableID = ?"
    return UDH.execute_query(q, (document_id, variable_id,))

# endregion <delete methods>
