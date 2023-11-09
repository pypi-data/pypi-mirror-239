import logging
import re
import time
from datetime import datetime
import psycopg2

import psycopg2.pool as psycopg2_pool
from migration.connector.source.enum import Column

from migration.connector.source.base import Source
from migration.base.exceptions import SourceExecutionError

logger = logging.getLogger(__name__)


class PGSource(Source):
    def __init__(self, config: dict, meta_conf_path=None, storage_conf_path=None):
        super().__init__('PostgreSQL', config)
        self.connection_params = self.get_connection_params()
        self.meta_conf_path = meta_conf_path
        self.storage_config_path = storage_conf_path
        pool_config = {'host': self.connection_params['host'], 'port': self.connection_params['port'],
                       'user': self.connection_params['user'], 'password': self.connection_params['password']}
        self.pool = psycopg2_pool.SimpleConnectionPool(minconn=10, maxconn=30, **pool_config)

    """
    PostgreSQL connection parameters is a dict including following keys:
    1. host: host of PG
    2. port: port for PG client
    3. database: database name
    4. user: user name
    5. passwd: password
    """

    def get_connection_params(self):
        assert self.config['host']
        assert self.config['user']
        assert self.config['password']
        assert self.config['port']

        return {
            'host': self.config['host'],
            'port': int(self.config['port']),
            'user': self.config['user'],
            'password': self.config['password'],
        }

    def connect(self):
        if self.connection is None:
            self.connection = psycopg2.connect(**self.connection_params)
            logger.info(f"Connect to PG {self.connection_params['host']} successfully")

    def get_database_names(self):
        result = self.execute_sql("show databases")
        return [row[0] for row in result]

    def get_table_names(self, database_name):
        result = self.execute_sql(f"show tables from {database_name}")
        return [row[0] for row in result]

    def get_ddl_sql(self, database_name, table_name):
        return self.execute_sql(f"show create table {database_name}.{table_name}")[0][1]

    def get_table_columns(self, database_name, table_name) -> list[Column]:
        result = self.execute_sql(f"desc {database_name}.{table_name}")
        table_columns = []
        for row in result:
            table_columns.append(Column(name=row[0], type=row[1].upper(),
                                        is_null=True if row[2].strip() == 'Yes' else False,
                                        default_value=row[4]))
        return table_columns

    def execute_sql(self, sql, bind_params=None):
        connection = self.pool.getconn()
        try:
            with connection.cursor() as cur:
                cur.execute(sql, bind_params)
                result = cur.fetchall()
                return result

        except SourceExecutionError as e:
            logger.error(f"PG connector execute sql {sql} failed, error: {e}")
            raise f"PG connector execute sql {sql} failed, error: {e}"
        except Exception as e:
            logger.error(f"PG connector execute sql {sql} failed, error: {e}")
            raise f"PG connector execute sql {sql} failed, error: {e}"
        finally:
            self.pool.putconn(connection)

    def type_mapping(self):
        return {
            'TIME': 'DATE',
            'CHARACTER': 'VARCHAR',
            'CHARACTER VARIATION': 'VARCHAR',
            'REAL': 'FLOAT',
            'DOUBLE PRECISION': 'DOUBLE',
            'INTEGER': 'INT',
        }

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
        if self.pool is not None:
            self.pool = None
        logger.info(f"Close connection to PG {self.connection_params['host']} successfully")

    def int_type_string(self):
        return 'INT'
