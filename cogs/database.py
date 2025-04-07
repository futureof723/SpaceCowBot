"""
Discord bot database extension.
This module provides database functionality for the bot, handling connections,
queries, and database schema management.
"""

import sqlite3
import logging
from discord.ext import commands

# Setup logger for error handling and database operations tracking
logger = logging.getLogger(__name__)


class Database(commands.Cog):
    """
    A Cog that manages the bot's database operations.

    This cog handles the SQLite database connection, provides helper methods for
    executing queries, and ensures proper database schema creation. It centralizes
    all database operations for the bot to maintain consistency and proper error handling.

    Attributes:
        bot (commands.Bot): The Discord bot instance.
        conn (sqlite3.Connection): The SQLite database connection.
        cursor (sqlite3.Cursor): The database cursor for executing queries.
    """

    def __init__(self, bot):
        """
        Initialize the Database cog and establish a database connection.

        Args:
            bot (commands.Bot): The Discord bot instance this cog is attached to.
        """
        self.bot = bot
        self.conn, self.cursor = self.initialize_database()

    def initialize_database(self):
        """
        Initialize the SQLite database and create necessary tables if they don't exist.

        Returns:
            tuple: A tuple containing (connection, cursor) for database operations.

        Raises:
            sqlite3.Error: If there's an issue connecting to or initializing the database.
        """
        try:
            # Create or connect to the SQLite database file
            conn = sqlite3.connect('study_points.db')

            # Configure row factory to return rows as dictionaries for easier access
            conn.row_factory = sqlite3.Row

            # Create a cursor for executing SQL commands
            c = conn.cursor()

            # Create the study_points table if it doesn't exist
            c.execute('''CREATE TABLE IF NOT EXISTS study_points (
                             user_id INTEGER PRIMARY KEY,
                             points INTEGER
                         )''')

            # Create the settings table if it doesn't exist
            c.execute('''CREATE TABLE IF NOT EXISTS settings (
                             key TEXT PRIMARY KEY,
                             value TEXT
                         )''')

            # Commit the changes to the database
            conn.commit()

            # Log successful initialization
            logger.info("SQLite database initialized successfully.")

            return conn, c
        except sqlite3.Error as e:
            # Log the error and re-raise it to be handled by the caller
            logger.error(f"Error connecting to SQLite database: {e}")
            raise

    def execute_query(self, query, params=()):
        """
        Execute an SQL query with error handling and automatic commit.

        This method executes the given SQL query with the provided parameters
        and commits the changes to the database. If an error occurs, it rolls
        back the transaction and logs the error.

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters to bind to the query. Defaults to empty tuple.

        Returns:
            None

        Note:
            This method automatically commits changes on success and rolls back on failure.
        """
        try:
            # Execute the query with the provided parameters
            self.cursor.execute(query, params)

            # Commit the changes to the database
            self.conn.commit()
        except sqlite3.Error as e:
            # Log the error
            logger.error(f"Database query error: {e}")

            # Roll back any changes to avoid partial updates
            self.conn.rollback()

    def fetch_query(self, query, params=()):
        """
        Execute a query and fetch all results with error handling.

        This method executes the given SQL query with the provided parameters
        and returns all matching rows. If an error occurs, it logs the error
        and returns an empty list.

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters to bind to the query. Defaults to empty tuple.

        Returns:
            list: A list of sqlite3.Row objects (dictionary-like) containing the query results,
                  or an empty list if an error occurs.
        """
        try:
            # Execute the query with the provided parameters
            self.cursor.execute(query, params)

            # Return all matching rows
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            # Log the error and return an empty list
            logger.error(f"Error fetching data: {e}")
            return []

    def cog_unload(self):
        """
        Perform cleanup when the cog is unloaded.

        This method is called automatically by discord.py when the cog is unloaded.
        It ensures that any pending database changes are committed and the connection
        is properly closed to prevent resource leaks.

        Returns:
            None
        """
        # Commit any pending changes
        self.conn.commit()

        # Close the database connection
        self.conn.close()


# Setup function to add the cog to the bot
async def setup(bot):
    """
    Setup function to add the Database cog to the bot.

    This function is called by Discord.py when the extension is loaded.

    Args:
        bot (commands.Bot): The bot instance to attach the cog to.

    Returns:
        None
    """
    await bot.add_cog(Database(bot))  # In discord.py 2.0+, this should be awaited