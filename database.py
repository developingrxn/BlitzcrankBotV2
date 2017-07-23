'''
Created on 17Jul.,2017

@author: Alex Palmer | SuperFrosty
'''
import sqlite3


class Database:
    """Default region handling"""

    database = ''
    cursor = ''

    def __init__(self, database: str):
        self.database = sqlite3.connect(database)
        self.cursor = self.database.cursor()

    def add_table(self, guild_id: str):
        """Add a table for a given guild"""
        try:
            self.cursor.execute('''
                                CREATE TABLE {}(sum_name TEXT, region TEXT)
                                '''.format("_" + guild_id)
                                )
            self.database.commit()
        except sqlite3.OperationalError:
            pass

    def add_user(self, guild_id: str, sum_name: str, region: str):
        """Add a given user and region to a given guild"""
        self.cursor.execute('''
                            INSERT INTO {}(sum_name, region)
                            VALUES(?,?)
                            '''.format("_" + guild_id), (sum_name.title(), region)
                            )
        self.database.commit()

    def find_user(self, guild_id: str, sum_name: str):
        """Find a given user in a given guild"""
        try:
            self.cursor.execute('''
                                SELECT region FROM {} WHERE sum_name = {}
                                '''.format("_" + guild_id, sum_name.title())
                                )
        except sqlite3.OperationalError:
            return None
        user = self.cursor.fetchone()
        return user[0]

    def add_entry(self, guild_id: int, region: str):
        """Add default region for a given guild"""
        self.cursor.execute('''
                            INSERT INTO guilds(guild_id, region)
                            VALUES(?,?)
                            ''', (guild_id, region)
                            )
        self.database.commit()

    def remove_entry(self, guild_id: int):
        """Remove default region for a given guild"""
        self.cursor.execute('''
                            DELETE FROM guilds WHERE guild_id = ?
                            ''', (guild_id,)
                            )
        self.database.commit()

    def update_entry(self, guild_id: int, region: str):
        """Update default region for a given guild"""
        self.cursor.execute('''
                            UPDATE guilds SET region = ? WHERE guild_id = ?
                            ''', (region, guild_id)
                            )
        self.database.commit()

    def find_entry(self, guild_id: int):
        """Find default region for a given guild"""
        self.cursor.execute('''
                            SELECT region FROM guilds WHERE guild_id = ?
                            ''', (guild_id,)
                            )
        region = self.cursor.fetchone()
        return region[0]

    def close_connection(self):
        """Close connection to database"""
        self.database.close()
