"""
Main script for updating the 'dateAdded' field for a specific Zotero item in an SQLite database.

This script initializes the `ZoteroInfoUpdate` class using a provided configuration, connects to the Zotero SQLite database, retrieves the item ID for a specified title, and updates the `dateAdded` field for that item. The script also logs important events and handles exceptions.

Usage:
    This script can be executed directly. Upon execution, it will:
    1. Log the start of the process.
    2. Connect to the Zotero SQLite database using the provided configuration.
    3. Fetch the item ID for the specified title.
    4. Update the `dateAdded` field for the retrieved item.
    5. Log success or failure and close the database connection.

Logging:
    The script uses Python's `logging` library to log information and errors at various stages of execution. The log level is set to `INFO`, with debug-level logs providing more granular details of the operations.

Exception Handling:
    Any unexpected errors encountered during the execution are caught, logged with detailed information, and re-raised for further handling.

Configuration:
    The script expects the `config` object (which contains the SQLite database path, new date to update, and title name) to be imported from the `zotero_info_update.config` module.

Example:
    Running this script will automatically perform the update:
        python main.py

Dependencies:
    - `zotero_info_update.zotero_info_update`: The main module responsible for database interactions.
    - `zotero_info_update.config`: The configuration module containing the database path, title name, and new date.
    - `zotero_info_update.logging_config`: A module for configuring logging settings (may be used for setup).
"""  # pylint: disable=line-too-long

if __name__ == "__main__":
    import logging
    from zotero_info_update.zotero_info_update import ZoteroInfoUpdate
    from zotero_info_update.config import config
    import zotero_info_update.logging_config  # pylint: disable=unused-import

    my_logger = logging.getLogger(__name__)
    my_logger.setLevel(logging.INFO)
    my_logger.info("Starting the ZoteroUpdateDateAdded script...")

    try:
        zotero_update_date_added = ZoteroInfoUpdate(config)
        my_logger.debug("Connecting to the database...")

        conn = zotero_update_date_added.connect_to_db()
        my_logger.debug("Connected to the database successfully.")

        # Fetch item ID
        my_logger.debug(
            "Fetching item ID for title: %s", zotero_update_date_added.title_name
        )
        itemId = zotero_update_date_added.get_item_id(conn)

        # my_logger.debug("Querying database for title...")
        # itemId = zotero_update_date_added.get_item_id(conn)
        # my_logger.debug("Item ID: %s", itemId)

        # Update date added
        zotero_update_date_added.update_date_added(conn)
        my_logger.info("Date added updated successfully.")

    except Exception as e:
        my_logger.error("An unexpected error occurred: %s", str(e), exc_info=True)
        raise

    finally:
        if conn:
            conn.close()
            my_logger.debug("Database connection closed.")
