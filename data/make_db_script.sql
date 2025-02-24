-------------------------------------------------
-------------------- TABLES ---------------------
-------------------------------------------------
-- PRAGMA case_sensitive_like = FALSE; deprecated in sqlite3
PRAGMA foreign_keys = ON;

-- Employers
-- Currently mostly optional; we'll see.
CREATE TABLE IF NOT EXISTS Employers (
    employerID    INTEGER PRIMARY KEY AUTOINCREMENT,
    employer_name TEXT NOT NULL UNIQUE,
    industry      TEXT     DEFAULT (NULL),
    location      TEXT     DEFAULT (NULL),
    notes         TEXT     DEFAULT (NULL),
    last_updated  DATETIME DEFAULT (datetime('now'))
);

-- Jobs
-- Main view for tracking job applications.
CREATE TABLE IF NOT EXISTS Jobs (
    jobID        INTEGER PRIMARY KEY AUTOINCREMENT,
    job_title    TEXT    NOT NULL,
    employerID   INTEGER NOT NULL,
    location     TEXT,
    URL          TEXT,
    status       TEXT                                                                                     DEFAULT 'applied',
    annual_pay   TEXT                                                                                     DEFAULT NULL,
--     TODO: annual pay should have min+max; currently changed to text for ease.
    ft_pt        TEXT    NOT NULL CHECK (ft_pt IN ('Full Time', 'Part Time'))                             DEFAULT 'Full Time',
    job_type     TEXT    NOT NULL CHECK (job_type IN ('Permanent', 'Contract', 'Temporary', 'Freelance')) DEFAULT 'Permanent',
    work_model   TEXT    NOT NULL CHECK (work_model IN ('In Person', 'Hybrid', 'Remote'))                 DEFAULT 'In Person',
    date_added   DATE                                                                                     DEFAULT (date('now')),
    date_applied DATE                                                                                     DEFAULT NULL,
    job_text     TEXT                                                                                     DEFAULT NULL,
    notes        TEXT                                                                                     DEFAULT NULL,
    archived     BOOLEAN                                                                                  DEFAULT FALSE,
    last_updated DATETIME                                                                                 DEFAULT (datetime('now')),
    FOREIGN KEY (employerID) REFERENCES Employers (employerID)
);

CREATE TABLE IF NOT EXISTS JobDocuments (
    documentID    INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_name      TEXT    NOT NULL, -- file name (nickname for use in the database)
    jobID         INTEGER NOT NULL,
    document_type TEXT    NOT NULL, -- resume, cover letter, etc.
    path          TEXT    NOT NULL, -- the absolute path including the name of the file
    date_created  DATETIME DEFAULT (datetime('now')),
    file_type     TEXT GENERATED ALWAYS AS (lower(substr(path, instr(path, '.') + 1))) STORED,
    FOREIGN KEY (jobID) REFERENCES Jobs (jobID) ON DELETE CASCADE
);

-- Documents.
-- Dependent on Jobs.
-- To keep storage to a reasonable minimum.
-- If a job is deleted, the related documents will also be deleted.
-- These are the processed and READY files; not templates.
CREATE TABLE IF NOT EXISTS Documents (
    documentID   INTEGER PRIMARY KEY AUTOINCREMENT,
    jobID        INTEGER NOT NULL,
    documentType TEXT    NOT NULL, -- resume, cover letter, etc.
    FOREIGN KEY (jobID) REFERENCES Jobs (jobID) ON DELETE CASCADE
);
-- The specific information of where each file is kept.
-- Some files will have multiple locations, and/or multiple file types (.docx and .pdf).
CREATE TABLE IF NOT EXISTS Document_Storage (
    storageID    INTEGER PRIMARY KEY AUTOINCREMENT,
    documentID   INTEGER NOT NULL,
    fileType     TEXT    NOT NULL, -- .pdf/.docx etc.
    path         TEXT    NOT NULL,
    file_name    TEXT    NOT NULL,
    date_created DATETIME DEFAULT (datetime('now')),
    FOREIGN KEY (documentID) REFERENCES Documents (documentID) ON DELETE RESTRICT
);

-- Variables
-- Stores reusable variables for resume and cover letter placeholders.
CREATE TABLE IF NOT EXISTS Variables (
    variableID    INTEGER PRIMARY KEY AUTOINCREMENT,
    variable_name TEXT NOT NULL UNIQUE
);

-- Variables and Documents
CREATE TABLE IF NOT EXISTS Document_Variables (
    documentID       INTEGER NOT NULL,
    variableID       INTEGER NOT NULL,
    placeholder_name text,
    PRIMARY KEY (documentID, variableID),
    FOREIGN KEY (documentID) REFERENCES Documents (documentID) ON DELETE CASCADE,
    FOREIGN KEY (variableID) REFERENCES Variables (variableID) ON DELETE RESTRICT
);

-------------------------------------------------
------------------- TRIGGERS --------------------
-------------------------------------------------

-- Trigger to update job status when applied date is set.
CREATE TRIGGER IF NOT EXISTS trigger_update_status_on_apply
    AFTER UPDATE OF date_applied
    ON Jobs
    WHEN NEW.date_applied IS NOT NULL
BEGIN
    UPDATE Jobs SET status = 'applied' WHERE jobID = NEW.jobID;
END;

-- Trigger to update the last_updated timestamp in Jobs
CREATE TRIGGER IF NOT EXISTS trigger_update_jobs
    AFTER UPDATE
    ON Jobs
BEGIN
    UPDATE Jobs SET last_updated = datetime('now') WHERE jobID = NEW.jobID;
END;

-- Trigger to update the last_updated timestamp in Employers
CREATE TRIGGER IF NOT EXISTS trigger_update_employers
    AFTER UPDATE
    ON Employers
BEGIN
    UPDATE Employers SET last_updated = datetime('now') WHERE employerID = NEW.employerID;
END;


