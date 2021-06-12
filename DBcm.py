# DBcm - database context manager
# This module is responsible for abstraction of the database connection with Python's DB-API.

# If we would like to change the underlying database system, only this code has to be changed and
# no code inside of the main module has to be edited.

import mysql.connector

class ConnectionError(Exception):
    # Occurs when the server cannot connect to the database
    pass


class CredentialsError(Exception):
    # Occurs when username or password to the database does not match
    pass


class SQLError(Exception):
    # Occurs when there is an error in SQL syntax
    pass


class UseDatabase:

    def __init__(self, dbconfig: dict) -> None:
        # Dictionary containing configuration for establishing connection with the database
        self.configuration = dbconfig

    def __enter__(self) -> 'cursor':
        try:
            self.conn = mysql.connector.connect(**self.configuration)   # Make a connection
            self.cursor = self.conn.cursor()                            # Create a database cursor
            return self.cursor
        except mysql.connector.errors.InterfaceError as err:
            raise ConnectionError(err)
        except mysql.connector.errors.ProgrammingError as err:
            raise CredentialsError(err)

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        # Force the database to write data
        self.conn.commit()
        # Tidy up
        self.cursor.close()     
        self.conn.close()

        # It is important for this part of code to be here, so in case of error,
        # the code above still executes and closes the connection.
        if exc_type is mysql.connector.errors.ProgrammingError:
            raise SQLError(exc_value)
        elif exc_type:
            raise exc_type(exc_value)