import sqlite3

class Database:
    """Default region handling"""
    database = ''
    cursor = ''
    def __init__(self, database: str):
        self.database = sqlite3.connect(database)
        self.cursor = self.database.cursor()

    def add_entry(self, guild_id: int, region: str):
        """Add default region for a given guild"""
        self.cursor.execute('''
                            INSERT INTO guilds(guild_id, region)
                            VALUES(?,?)
                            ''', (guild_id, region))
        self.database.commit()

    def remove_entry(self, guild_id: int):
        """Remove default region for a given guild"""
        self.cursor.execute('''
                            DELETE FROM guilds WHERE guild_id = ?
                            ''', (guild_id,))
        self.database.commit()

    def update_entry(self, guild_id: int, region: str):
        """Update default region for a given guild"""
        self.cursor.execute('''
                            UPDATE guilds SET region = ? WHERE guild_id = ?
                            ''', (region, guild_id))
        self.database.commit()

    def find_entry(self, guild_id: int):
        """Find default region for a given guild"""
        self.cursor.execute('''
                            SELECT region FROM guilds WHERE guild_id = ?
                            ''', (guild_id,))
        region = self.cursor.fetchone()
        return region[0]

    def close_connection(self):
        """Close connection to database"""
        self.database.close()
