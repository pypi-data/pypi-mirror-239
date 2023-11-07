import unittest

from unittest.mock import patch
from capsphere.data.db.postgres.connection import PostgreSQLConnection


class TestConnection(unittest.TestCase):

    @patch('capsphere.data.db.postgres.connection.os.getenv')
    def test_missing_environment_variables(self, mock_getenv):
        mock_getenv.return_value = None

        # Attempt to instantiate the connection, which should raise EnvironmentError
        with self.assertRaises(EnvironmentError) as context:
            connection = PostgreSQLConnection(ssl_cert_path='/path/to/cert')

        # Check if the error message is correct
        self.assertIn("The environment variable DB_HOST is not set", str(context.exception))

    # def test_postgres(self):
    #     # pg_db = PostgreSQLConnection(ssl_cert_path=self.pem_path)
    #     pg_db = PostgreSQLConnection()
    #     try:
    #         connection = pg_db.connect()
    #         print("Connection successful.")
    #     except Exception as e:
    #         print(f"Connection failed: {e}")
    #     finally:
    #         if pg_db.connection:
    #             pg_db.disconnect()
