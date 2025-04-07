import sqlite3
import logging
from discord.ext import commands

# Setup logger for error handling
logger = logging.getLogger(__name__)

class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn, self.cursor = self.initialize_database()

    def initialize_database(self):
        try:
            conn = sqlite3.connect('study_points.db')
            conn.row_factory = sqlite3.Row  # Enable dictionary cursor to fetch rows as dicts
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS study_points (
                             user_id INTEGER PRIMARY KEY,
                             points INTEGER
                         )''')
            c.execute('''CREATE TABLE IF NOT EXISTS settings (
                             key TEXT PRIMARY KEY,
                             value TEXT
                         )''')
            conn.commit()
            logger.info("SQLite database initialized successfully.")
            return conn, c
        except sqlite3.Error as e:
            logger.error(f"Error connecting to SQLite database: {e}")
            raise

    # A helper method to execute queries with error handling
    def execute_query(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Database query error: {e}")
            self.conn.rollback()  # Rollback on failure

    # A helper method to fetch query results with error handling
    def fetch_query(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Error fetching data: {e}")
            return []


    # Clean up the database connection when the cog is unloaded
    def cog_unload(self):
        self.conn.commit()  # Commit any pending changes
        self.conn.close()  # Close the connection

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(Database(bot))  # This should NOT be awaited
