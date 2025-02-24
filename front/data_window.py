from flet import Text, Tabs, Tab, Icon, Row
from flet.core.icons import Icons
from flet.core.types import VerticalAlignment, CrossAxisAlignment

from front.controls.database_view import DatabaseView


def data_window():
    jobs_table = DatabaseView('data/applications.sqlite', 'Jobs',
                              select_query=r'''
                       SELECT jobID                 as ID,
                       job_title                    as Title,
                       e.employer_name              as Employer,
                       j.location                   as Location,
                       URL,
                       annual_pay                   as Salary,
                       ft_pt                        as 'Ft/Pt',
                       job_type                     as 'Job Type',
                       work_model                   as Format,
                       strftime('%F', date_added)   as Added,
                       strftime('%F', date_applied) as 'Applied on',
                       strftime('%F', j.last_updated) as 'Updated',
                       j.notes as Notes
                        FROM Jobs j
                         JOIN Employers e on e.employerID = j.employerID'''
                              , column_names=['ID',
                                              'Title',
                                              'Employer',
                                              'Location',
                                              'URL',
                                              'Salary',
                                              'Ft/Pt',
                                              'Job Type',
                                              'Format',
                                              'Added',
                                              'Applied on',
                                              'Updated', ])
    employers_table = DatabaseView('data/applications.sqlite', 'Employers',
                                   select_query=r'''SELECT employerID as 'ID', 
                                   employer_name as 'Employer',  
                                   industry as 'Industry',  
                                   location as 'Location', 
                                    notes as 'Notes',
                                     last_updated as 'Last Updated'
                                      FROM Employers ''',
                                   column_names=['ID',
                                                 'Employer',
                                                 'Industry',
                                                 'Location',
                                                 'Notes',
                                                 'Last Updated'])
    documents_table = DatabaseView('data/applications.sqlite', 'Documents', r"""
SELECT Documents.jobID                                                AS 'ID',
       Employers.employer_name                                        AS 'Employer',
       Jobs.job_title                                                 AS 'Title',
       Documents.documentType                                         AS 'Document Type',
       Document_Storage.file_name                                     AS 'File Name',
       concat(Document_Storage.path, '\', Document_Storage.file_name) AS 'Path'
FROM Jobs
         INNER JOIN Documents ON Documents.jobID = Jobs.jobID
         JOIN Document_Storage ON Documents.documentID = Document_Storage.documentID
         LEFT JOIN Employers on Jobs.employerID = Employers.employerID """,
                                   column_names=['ID',
                                                 'Employer',
                                                 'Title',
                                                 'Document Type',
                                                 'File Name',
                                                 'Path']
                                   )
    t = Tabs(
        selected_index=0, animation_duration=300,
        tabs=[
            Tab(tab_content=
                Row([Icon(Icons.WORK), Text("Jobs")], expand=True, vertical_alignment=CrossAxisAlignment.START),
                content=jobs_table),
            Tab(tab_content=
                Row([Icon(Icons.BUSINESS), Text("Employers")], expand=True,
                    vertical_alignment=CrossAxisAlignment.START),
                content=employers_table),
            Tab(tab_content=
                Row([Icon(Icons.FILE_OPEN), Text("Documents")], expand=True,
                    vertical_alignment=CrossAxisAlignment.START),
                content=documents_table)])
    return t
