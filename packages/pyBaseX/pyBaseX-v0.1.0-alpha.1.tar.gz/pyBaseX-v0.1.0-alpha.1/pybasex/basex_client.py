import requests
from functools import wraps

import errors as pbx_errors
import utils as pbx_utils
import utils.xml_utils as pbx_xml_utils
from fragments import build_query_fragment


class BaseXClient(object):

    def __init__(self, url, default_database=None,
                 user=None, password=None, logger=None):
        self.url = url
        self.default_database = default_database
        self.user = user
        self.password = password
        self.logger = logger or pbx_utils.get_logger('basex_client')
        self.session = None

    def __del__(self):
        self.disconnect()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        return None

    def connect(self):
        self.logger.debug('Creating session')
        self.session = requests.Session()
        if self.user and self.password:
            self.session.auth = (self.user, self.password)

    def disconnect(self):
        self.logger.debug('Closing session')
        if self.session:
            self.session.close()
        self.session = None

    def errors_handler(f):
        @wraps(f)
        def wrapper(inst, *args, **kwargs):
            inst._check_connection()
            try:
                return f(inst, *args, **kwargs)
            except requests.ConnectionError, ce:
                inst.logger.exception(ce)
                raise pbx_errors.ConnectionError('Unable to connect to "%s"' % inst.url)
        return wrapper

    @property
    def connected(self):
        return not(self.session is None)

    def _check_connection(self):
        if not self.connected:
            raise pbx_errors.ConnectionClosedError('Connection closed')

    def _build_url(self, database, item=None):
        url = '/'.join([self.url, database])
        if item:
            url = '/'.join([url, item])
        return url

    def _resolve_database(self, database_name=None):
        db = database_name or self.default_database
        if db is None:
            raise pbx_errors.ConfigurationError('Missing default database')
        return db

    def _handle_wrong_url(self):
        msg = 'Unable to complete the request, "%s" is not a valid BaseX REST URL' % self.url
        self.logger.error(msg)
        raise pbx_errors.InvalidURLError(msg)

    def _check_url(self, database):
        # check for invalid BaseX URL
        _ = self.get_databases()
        # URL is a valid one, database does not exist
        raise pbx_errors.UnknownDatabaseError('Database "%s" does not exist' % database)

    def _wrap_results(self, res_text):
        res_text = '<results>{0}</results>'.format(res_text)
        return pbx_xml_utils.str_to_xml(res_text)

    # --- objects creation methods
    @errors_handler
    def create_database(self, database=None):
        db = self._resolve_database(database)
        self.logger.debug('Creating database "%s"' % db)
        if db not in self.get_databases():
            response = self.session.put(self._build_url(db))
        else:
            raise pbx_errors.OverwriteError('Database "%s" already exists' % db)
        if response.status_code == requests.codes.not_found:
            self._handle_wrong_url()
        self.logger.info('RESPONSE (status code %d): %s', response.status_code, response.text)

    @errors_handler
    def add_document(self, xml_doc, document_id, database=None):
        db = self._resolve_database(database)
        if document_id in self.get_resources(db):
            raise pbx_errors.OverwriteError('A document with ID "%s" already exists in database "%s"' %
                                            (document_id, db))
        xml_doc = pbx_xml_utils.xml_to_str(xml_doc)
        self.logger.debug('Saving document %s' % xml_doc)
        response = self.session.put(self._build_url(db, document_id), xml_doc)
        self.logger.info('RESPONSE (status code %d): %s', response.status_code, response.text)

    # --- objects retrieval methods
    @errors_handler
    def get_databases(self):
        response = self.session.get(self.url)
        if response.status_code == requests.codes.not_found:
            self._handle_wrong_url()
        results = pbx_xml_utils.str_to_xml(response.text)
        dbs_map = {}
        for ch in results.getchildren():
            dbs_map[ch.text] = {
                'size': ch.get('size'),
                'resources': ch.get('resources')
            }
        return dbs_map

    @errors_handler
    def get_resources(self, database=None):
        db = self._resolve_database(database)
        response = self.session.get(self._build_url(db))
        if response.status_code == requests.codes.not_found:
            self._check_url(db)
        results = pbx_xml_utils.str_to_xml(response.text)
        res_map = {}
        for ch in results.getchildren():
            res_map[ch.text] = {
                'type': ch.get('type'),
                'content-type': ch.get('content-type'),
                'size': ch.get('size')
            }
        return res_map

    @errors_handler
    def get_document(self, document_id, database=None):
        db = self._resolve_database(database)
        response = self.session.get(self._build_url(db, document_id))
        if response.status_code == requests.codes.not_found:
            self._check_url(db)
        result = pbx_xml_utils.str_to_xml(response.text)
        if result.tag == '{http://basex.org/rest}databases' and result.get('resources') == 0:
            self.logger.info('There is not document with ID "%s" in database "%s"' % (document_id, db))
            return None
        else:
            return result

    # --- objects deletion methods
    @errors_handler
    def delete_database(self, database=None):
        db = self._resolve_database(database)
        response = self.session.delete(self._build_url(db))
        if response.status_code == requests.codes.not_found:
            self._check_url(db)

    @errors_handler
    def delete_document(self, document_id, database=None):
        db = self._resolve_database(database)
        response = self.session.delete(self._build_url(db, document_id))
        if response.status_code == requests.codes.not_found:
            self._check_url(db)

    # --- commands\queries execution methods
    @errors_handler
    def execute_query(self, query, database=None):
        db = self._resolve_database(database)
        q_frag = build_query_fragment(query)
        response = self.session.post(self._build_url(db),
                                     pbx_utils.xml_utils.xml_to_str(q_frag))
        if response.status_code == requests.codes.not_found:
            self._check_url(db)
        if response.status_code == requests.codes.bad:
            raise pbx_errors.QueryError('Query error: ' + response.text.replace('\n', ' '))
        return self._wrap_results(response.text)
