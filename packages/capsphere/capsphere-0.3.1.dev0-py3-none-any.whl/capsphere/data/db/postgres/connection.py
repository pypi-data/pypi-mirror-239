import logging
import os
import psycopg2

from capsphere.data.db.exception import DatabaseExecutionError, DatabaseConnectionError
from capsphere.data.db.interface import BaseDBConnection


class PostgreSQLConnection(BaseDBConnection):
    def __init__(self, ssl_cert_path=None):
        self.logger = logging.getLogger(__name__)

        env_vars = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_PORT']
        for var in env_vars:
            if os.getenv(var) is None:
                message = f"The environment variable {var} is not set. It is required for Postgres database connection."
                self.logger.error(message)
                raise EnvironmentError(message)

        super().__init__(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=int(os.getenv('DB_PORT', 5432))
        )
        self.ssl_cert_path = ssl_cert_path

    def connect(self):
        if not self.connection:
            try:
                sslmode = 'require' if self.ssl_cert_path else 'prefer'
                connection_args = {
                    "host": self.host,
                    "database": self.database,
                    "user": self.user,
                    "password": self.password,
                    "port": self.port,
                    "sslmode": sslmode,
                }
                if self.ssl_cert_path:
                    connection_args["sslrootcert"] = self.ssl_cert_path

                self.connection = psycopg2.connect(**connection_args)
            except psycopg2.OperationalError as e:
                self.logger.error(f"Database connection failed: {e}")
                raise DatabaseConnectionError(e)
        return self.connection

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, fetch_results=True):
        connection = self.connect()
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            connection.commit()
            if fetch_results:
                result = cursor.fetchall()
        except psycopg2.Error as e:
            connection.rollback()
            self.logger.error(f"Query execution failed: {e}")
            raise DatabaseExecutionError(e)
        finally:
            cursor.close()
            self.disconnect()
        return result
