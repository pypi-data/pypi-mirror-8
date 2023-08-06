# -*- coding: utf-8 -*-
#
# Input classes for ETL, databases.
#
# Author: Just van den Broecke
#
from stetl.component import Config
from stetl.input import Input
from stetl.util import Util
from stetl.packet import FORMAT
from stetl.postgis import PostGIS

log = Util.get_log('dbinput')


class DbInput(Input):
    """
    Input from any database (abstract base class).
    """

    def __init__(self, configdict, section, produces):
        Input.__init__(self, configdict, section, produces=produces)

    def read(self, packet):
        return packet


class SqlDbInput(DbInput):
    """
    Input using a query from any SQL-based RDBMS (abstract base class).
    """

    # Start attribute config meta
    @Config(ptype=str, required=True, default=None)
    def database_name(self):
        """
        Database name
        """
        pass

    @Config(ptype=str, required=False, default=None)
    def table(self):
        """
        Table name
        """
        pass

    @Config(ptype=str, required=False, default=None)
    def column_names(self):
        """
        Column names to populate records with. If empty taken from table metadata.
        """
        pass

    @Config(ptype=bool, required=False, default=False)
    def read_once(self):
        """
        Read once? i.e. only do query once and stop
        """
        pass

    @Config(ptype=str, required=False, default=None)
    def query(self):
        """
        The query (string) to fire.
        """
        pass
    # End attribute config meta

    def __init__(self, configdict, section, produces):
        DbInput.__init__(self, configdict, section, produces=produces)
        self.columns = self.column_names
        self.select_all = "select * from %s" % self.table

    def result_to_output(self, db_records):
        """
        Convert DB-specific record iterator to single Python record (dict) or record array (list of dict).

        """

        # record is Python list of Python dict (multiple records)
        records = list()

        # Convert list of lists to list of dict using column_names
        for db_record in db_records:
            records.append(dict(zip(self.columns, db_record)))

        # We may have specified a single record output_format in rare cases
        if self.output_format == FORMAT.record:
            if len(records) > 0:
                return records[0]
            else:
                return None
        else:
            return records

    def do_query(self, query_str):
        """
        DB-neutral query returning Python record list.
        """

        # Perform DB-specific query
        db_records = self.raw_query(query_str)

        # Convert query result to record_array
        return self.result_to_output(db_records)

    def raw_query(self, query_str):
        """
        Performs DB-specific  query and returns raw records iterator.
        """
        pass

    def read(self, packet):

        # Perform DB-specific query
        packet.data = self.do_query(self.query)

        # No more records to process?
        if len(packet.data) == 0 or self.read_once is True:
            packet.set_end_of_stream()
            log.info('Nothing to do. All file_records done')
            return packet

        return packet


class PostgresDbInput(SqlDbInput):
    """
    Input by querying records from a Postgres database.
    Input is a query, like SELECT * from mytable.
    Output is zero or more records as record array (array of dict) or single record (dict).

    produces=FORMAT.record_array (default) or FORMAT.record
    """

    # Start attribute config meta
    @Config(ptype=str, required=False, default='localhost')
    def host(self):
        """
        host name or host IP-address
        """
        pass

    @Config(ptype=str, required=False, default='postgres')
    def user(self):
        """
        User name
        """
        pass

    @Config(ptype=str, required=False, default='postgres')
    def password(self):
        """
        User password
        """
        pass

    @Config(ptype=str, required=False, default='public')
    def schema(self):
        """
        Schema (postgres schema) name
        """
        pass
    # End attribute config meta

    def __init__(self, configdict, section):
        SqlDbInput.__init__(self, configdict, section, produces=[FORMAT.record_array, FORMAT.record])
        self.db = None

    def init(self):
        # Connect only once to DB
        log.info('Init: connect to DB')
        self.db = PostGIS(self.cfg.get_dict())
        self.db.connect()

        # If no explicit column names given, get from DB meta info
        self.columns = self.column_names
        if self.column_names is None:
            self.columns = self.db.get_column_names(self.cfg.get('table'), self.cfg.get('schema'))

    def exit(self):
        # Disconnect from DB when done
        log.info('Exit: disconnect from DB')

        self.db.disconnect()

    def raw_query(self, query_str):

        self.db.execute(query_str)

        db_records = self.db.cursor.fetchall()
        log.info('read recs: %d' % len(db_records))

        return db_records

class SqliteDbInput(SqlDbInput):
    """
    Input by querying records from a SQLite database.
    Input is a query, like SELECT * from mytable.
    Output is zero or more records as record array (array of dict) or single record (dict).

    produces=FORMAT.record_array (default) or FORMAT.record
    """

    def __init__(self, configdict, section):
        SqlDbInput.__init__(self, configdict, section, produces=[FORMAT.record_array, FORMAT.record])
        self.db = None

        import sqlite3
        self.sqlite = sqlite3

    def get_conn(self):
        # Database name is the filepath
        log.info('Connect to SQLite DB: %s' % self.database_name)
        return self.sqlite.connect(self.database_name)

    def init(self):
        # If no explicit column names given, get from DB meta info
        if self.column_names is None:
            # Connect only once to DB
            conn = self.get_conn()
            cursor = conn.cursor()
            cursor.execute(self.select_all)
            self.columns = [f[0] for f in cursor.description]
            conn.close()

    def raw_query(self, query_str):
        # We open and close immediately. TODO: maybe this is not necessary i.e. once in init/exit.
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(query_str)
        db_records = cursor.fetchall()
        log.info('%d records read' % len(db_records))
        conn.close()

        return db_records