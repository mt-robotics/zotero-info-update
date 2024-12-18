"""
Configuration module for the Zotero item date update process.

This module contains the configuration settings required for updating the 'dateAdded' field of a specific Zotero item in the SQLite database. It loads sensitive configuration data from environment variables and defines key parameters such as the Zotero database path, the new date to set for the item, and the title of the item to search for.

Usage:
    The `config` dictionary is used by the `ZoteroInfoUpdate` class to perform database operations, such as connecting to the Zotero SQLite database and updating the 'dateAdded' field for a specific item.

Manual Update Section:
    - `TITLE_NAME`: The title of the Zotero item to search for (must be updated manually).
    - `NEW_DATE_ADDED`: The new date to set for the selected item (must be updated manually).
    
    These parameters can be customized for each update operation.

Environment Variables:
    - `DB_PATH`: The path to the Zotero SQLite database. This is loaded from the environment variable `DB_PATH`.

Configuration Dictionary (`config`):
    The configuration dictionary contains:
    - `db_path`: The path to the Zotero SQLite database, loaded from the environment.
    - `new_date_added`: The new date to update in the database.
    - `title_name`: The title of the item to search for in the database.

Example:
    - To use this configuration, ensure that `DB_PATH` is set in your environment, and then the `config` dictionary will be populated for use by the main update script.

"""  # pylint: disable=line-too-long

import os
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------MANUAL UPDATE: Start---------------------------------------
# Specify the title name to search
TITLE_NAME = (
    # "What are ethical frameworks?"
    # "The Design Of Everyday Things"
    # "A Unified Framework of Five Principles for AI in Society"
    # "Aristotle & Virtue Theory"
    # "Human-Centered AI: A New Synthesis"
    "The Artiﬁcial Intelligence of the Ethics"
)

# Update the "Date Added" for a specific item
NEW_DATE_ADDED = "2024-11-30 09:57:32"  # UTC time = GMT+7 - 7hours
# ---------------------------------------MANUAL UPDATE: End---------------------------------------

# Specify the path to your zotero.sqlite file
DB_PATH = os.getenv("DB_PATH")


# Create a dictionary to store the configuration for dependency injection
config = {
    "db_path": DB_PATH,
    "new_date_added": NEW_DATE_ADDED,
    "title_name": TITLE_NAME,
}
