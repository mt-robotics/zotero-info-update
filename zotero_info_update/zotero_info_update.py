"""
Module for updating Zotero item information in an SQLite database.

This module provides the `ZoteroInfoUpdate` class, which allows users to connect to a Zotero SQLite database, retrieve an item ID based on a given title, and update the `dateAdded` field for that item.

Classes:
    ZoteroInfoUpdate: A class responsible for interacting with the Zotero SQLite database, including fetching item IDs based on title names and updating the `dateAdded` field.

Functions:
    None (all functionality is encapsulated within the `ZoteroInfoUpdate` class).

Usage:
    1. Create an instance of `ZoteroInfoUpdate` by providing a configuration dictionary with keys:
        - `db_path`: The path to the SQLite database.
        - `new_date_added`: The new date to update in the `dateAdded` field.
        - `title_name`: The title name to search for in the database.
    2. Call `connect_to_db()` to establish a connection to the database.
    3. Use `get_item_id(conn)` to fetch the item ID based on the provided title.
    4. Call `update_date_added(conn)` to update the `dateAdded` field for the fetched item.

Logging:
    The module uses Python's `logging` library to log information, errors, and other relevant events. The log level is set to `INFO`, and detailed error information is logged for any exceptions encountered.

Exception Handling:
    The class methods handle various SQLite-related errors such as `OperationalError`, `DatabaseError`, and `IntegrityError`. In case of unexpected errors, they are logged and re-raised for further handling.

Example:
    config = {
        "db_path": "/path/to/zotero/database",
        "new_date_added": "2024-12-18",
        "title_name": "Understanding Ethics"
    }
    
    zotero_update = ZoteroInfoUpdate(config)
    conn = zotero_update.connect_to_db()
    zotero_update.update_date_added(conn)

Author:
    Monireach Tang

Version:
    1.0

Date:
    2024-12-18
"""  # pylint: disable=line-too-long

import sqlite3
import logging
import zotero_info_update.logging_config  # pylint: disable=unused-import

# Configure logging
my_logger = logging.getLogger(__name__)
my_logger.setLevel(logging.INFO)


class ZoteroInfoUpdate:
    """
    A class to update Zotero information.

    Attributes:
        config (dict): The configuration dictionary.
        db_path (str): The path to the SQLite database.
        new_date_added (str): The new date added for the item.
        title_name (str): The title name to search for.

    Methods:
        __init__(cfg): Initializes the class with the provided configuration.
        connect_to_db(): Establish a connection to the SQLite database.
        get_item_id(conn): Retrieves the item ID from the database based on the title name.
        update_date_added(conn): Updates the date added for the item in the database.
    """

    def __init__(self, cfg):
        self.config = cfg
        self.db_path = self.config.get("db_path")
        self.new_date_added = self.config.get("new_date_added")
        self.title_name = self.config.get("title_name")

    def connect_to_db(self):
        """Establish a connection to the SQLite database."""

        my_logger.debug("Database path: %s", self.db_path)

        # Connect to the SQLite database
        try:
            conn = sqlite3.connect(self.db_path)
            return conn

        except sqlite3.OperationalError as e:
            my_logger.error("SQLite OperationalError: %s", e, exc_info=True)
            raise  # Re-raise the exception so the calling code knows the connection failed.

        except (
            sqlite3.DatabaseError
        ) as e:  # Catches other sqlite3 database-related errors
            my_logger.error("SQLite DatabaseError: %s", e, exc_info=True)
            raise

        except Exception as e:
            my_logger.error("An unexpected error occurred: %s", str(e), exc_info=True)
            raise

    def get_item_id(self, conn):
        """
        Retrieves the item ID from the database based on the title name.

        Args:
            conn: The connection to the SQLite database.

        Returns:
            int: The item ID if found, otherwise raises a ValueError.

        Raises:
            ValueError: If the title name is None or empty.
            sqlite3.OperationalError: If a database error occurs.
            sqlite3.IntegrityError: If a database integrity error occurs.
            sqlite3.ProgrammingError: If a programming error occurs.
            sqlite3.InterfaceError: If a database interface error occurs.
            sqlite3.DataError: If a database data error occurs.
            sqlite3.DatabaseError: If a database-related error occurs.
            ValueError: If no matching item is found.
        """

        if not self.title_name:
            raise ValueError("Title name cannot be None or empty.")

        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT i.itemID, id.valueID, idv.value, i.dateAdded, i.clientDateModified
                FROM itemDataValues idv
                INNER JOIN itemData id ON id.valueID = idv.valueID
                INNER JOIN items i ON i.itemID = id.itemID
                WHERE idv.value LIKE ?
                """,
                ("%" + self.title_name + "%",),
            )

            # Fetch and return results
            results = cursor.fetchall()

            if not results:
                my_logger.error("No matching item found for title: %s", self.title_name)
                raise ValueError(f"No matching item found for title: {self.title_name}")

            my_logger.info(
                "Successfully fetched results for title: %s", self.title_name
            )
            my_logger.info(
                "Results: %s", results[0]
            )  # Sample Output: (53, 385, 'What are ethical frameworks?')
            return results[0][0]

        # except sqlite3.OperationalError as e:
        #     my_logger.error("SQLite OperationalError: %s", e, exc_info=True)
        #     raise  # Re-raise the exception so the calling code knows the connection failed.

        # except sqlite3.IntegrityError as e:
        #     my_logger.error("SQLite IntegrityError: %s", e, exc_info=True)
        #     raise

        # except sqlite3.ProgrammingError as e:
        #     my_logger.error("SQLite ProgrammingError: %s", e, exc_info=True)
        #     raise

        # except sqlite3.InterfaceError as e:
        #     my_logger.error("SQLite InterfaceError: %s", e, exc_info=True)
        #     raise

        # except sqlite3.DataError as e:
        #     my_logger.error("SQLite DataError: %s", e, exc_info=True)
        #     raise

        except (
            sqlite3.DatabaseError
        ) as e:  # Catches other sqlite3 database-related errors
            my_logger.error("SQLite DatabaseError: %s", e, exc_info=True)
            raise

        except ValueError as e:
            my_logger.error("ValueError: Invalid input - %s", e, exc_info=True)
            raise

        except MemoryError as e:
            my_logger.critical("MemoryError: Out of memory - %s", e, exc_info=True)
            raise

        except Exception as e:
            my_logger.error("An unexpected error occurred: %s", str(e), exc_info=True)
            raise

        finally:
            my_logger.info("Database connection closed.")

    def update_date_added(self, conn):
        """
        Update the date added for the item in the database.

        Args:
            conn: The connection to the SQLite database.

        Raises:
            ValueError: If the item ID is None or empty.
            sqlite3.DatabaseError: If a database-related error occurs.
            ValueError: If an invalid input error occurs.
            MemoryError: If an out-of-memory error occurs.

        """

        item_id = self.get_item_id(conn)

        if not item_id:
            my_logger.error("Item ID not found for title: %s", self.title_name)

        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE items SET dateAdded = ? WHERE itemID = ?
                """,
                (self.new_date_added, item_id),
            )
            conn.commit()

        except (
            sqlite3.DatabaseError
        ) as e:  # Catches other sqlite3 database-related errors
            my_logger.error("SQLite DatabaseError: %s", e, exc_info=True)
            raise

        except ValueError as e:
            my_logger.error("ValueError: Invalid input - %s", e, exc_info=True)
            raise

        except MemoryError as e:
            my_logger.critical("MemoryError: Out of memory - %s", e, exc_info=True)
            raise

        except Exception as e:
            my_logger.error("An unexpected error occurred: %s", str(e), exc_info=True)
            raise

        finally:
            my_logger.info("Database connection closed.")
