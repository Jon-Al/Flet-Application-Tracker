from utils.database_handler import DatabaseHandler
from utils.path_utils import PathManager, PathFlag

from utils.simple_logger import SimpleLogger

UNIVERSAL_DATABASE_HANDLER = (
    DatabaseHandler('data/applications.sqlite', creation_script_path='data/make_db_script.sql'))

LOGGER = SimpleLogger('log.log')

DOCS_TEMPLATES = PathManager('docs/templates', PathFlag.FROM_PROJECT_ROOT | PathFlag.CREATE_FOLDER)
DOCS_APPLICATIONS = PathManager('docs/Applications',
                                PathFlag.FROM_PROJECT_ROOT | PathFlag.CASCADE_BY_DATE | PathFlag.CREATE_FOLDER)
PDF_FOLDER = PathManager('PDF Output', PathFlag.FROM_PROJECT_ROOT | PathFlag.CREATE_FOLDER)
RESOURCES_FOLDER = PathManager('resources', PathFlag.FROM_PROJECT_ROOT)
DATA_FOLDER = PathManager('data', PathFlag.FROM_PROJECT_ROOT)
PLACEHOLDERS_FOLDER = PathManager('data/placeholders', PathFlag.FROM_PROJECT_ROOT)
