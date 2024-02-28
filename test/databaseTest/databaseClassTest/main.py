import sqlite3


class Database:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.execute("PRAGMA foreign_keys = ON")
        self.c = self.db.cursor()

        self.c.execute("""CREATE TABLE IF NOT EXISTS Environments
            (EID                INTEGER     PRIMARY KEY,
            gravity             REAL        NOT NULL,
            air_density         REAL)""")

        self.c.execute("""CREATE TABLE IF NOT EXISTS Projectiles
            (PID                INTEGER     PRIMARY KEY,
            mass                REAL,
            drag_coefficient    REAL,
            area                REAL)""")

        self.c.execute("""CREATE TABLE IF NOT EXISTS Motion
            (MID                INTEGER     PRIMARY KEY,
            velocity            REAL        NOT NULL,
            ele_angle           REAL        NOT NULL,
            azi_angle           REAL        NOT NULL,
            x                   REAL        NOT NULL,
            y                   REAL        NOT NULL,
            z                   REAL        NOT NULL)""")

        self.c.execute("""CREATE TABLE IF NOT EXISTS Presets
            (name               TEXT        PRIMARY KEY,
            drag                TEXT        NOT NULL,
            EID                 INTEGER     NOT NULL,
            PID                 INTEGER     NOT NULL,
            MID                 INTEGER     NOT NULL,
            FOREIGN KEY (EID) REFERENCES Environments (EID),
            FOREIGN KEY (PID) REFERENCES Projectiles (PID),
            FOREIGN KEY (MID) REFERENCES Motion (MID))""")
        self.db.commit()  # Saves any changes

    def insertRecord(self, table, data):
        """
        Adds a record into a specified table
        :param table: The name of the table
        :type table: str
        :param data: The data to be inserted into the table
        :type data: dict[str]
        :return: None
        """
        fields = list(data.keys())
        values = list(data.values())
        q_marks = ", ".join(["?"] * len(data))
        print(f"INSERT INTO {table} ({", ".join(fields)}) VALUES ({", ".join(map(str, values))})")
        self.c.execute(f"INSERT INTO {table} ({", ".join(fields)}) VALUES ({q_marks})", values)
        self.db.commit()

    def selectRecord(self, field, table, data):
        """
        Selects a record from a specified table
        :param field: The field to be fetched
        :param table: The table in the database
        :type table: str
        :param data: The data of the record
        :type data: dict[str]
        :return: The value in the field
        :rtype: list
        """
        fields = list(data.keys())
        values = list(data.values())
        q_marks = ", ".join(["?"] * len(data))
        self.c.execute(f"SELECT {field} FROM {table} WHERE ({q_marks}) IS ({str(*values)})", values)
        return self.c.fetchall()

    def duplicateCheck(self, primary_key, table, data):
        """
        Checks for records in the table. If the record does not exist, the values are inserted into the table. Returns
        the primary key of the record with the specified values
        :param primary_key: The primary key of the table
        :param table: The name of the table
        :type table: str
        :param data: The data in the record
        :type data: dict[str]
        :return: The primary key of the record
        """
        primary_key = self.selectRecord(primary_key, table, data)  # Selects the primary key from the record
        if not primary_key:  # If the record does not exist
            self.insertRecord(table, data)  # Inserts the record
            primary_key = self.selectRecord(primary_key, table, data)[0][0]  # Fetches the primary key of the new record
        else:  # If the record exists
            primary_key = primary_key[0][0]  # Isolates the primary key from the record
        return primary_key

    def selectPreset(self, name):
        """
        Fetches all the values in the preset from the different tables
        :param name: The name of the preset
        :type name: str
        :return: The values in the preset
        :rtype: tuple[str | float | None]
        """
        # Selects all the values from the preset
        self.c.execute("""SELECT Presets.drag, 
        Motion.velocity, Motion.ele_angle, Motion.azi_angle, Motion.x, Motion.y, Motion.z, 
        Environments.gravity, Environments.air_density,
        Projectiles.mass, Projectiles.drag_coefficient, Projectiles.area
        FROM Motion, Environments, Presets, Projectiles 
        WHERE Presets.EID=Environments.EID AND Presets.PID=Projectiles.PID AND Presets.MID=Motion.MID AND 
        Presets.name=?""", [name])
        return self.c.fetchall()[0]

    def deleteRecord(self, table, primary_key, field):
        """
        Deletes a record from a table.
        :param table: The table which the record is being deleted from
        :type table: str
        :param primary_key: The primary key of the record to be deleted
        :param field: The name of the primary field
        """
        self.c.execute(f"DELETE FROM {table} WHERE ({field}) IS ({primary_key})")
        self.db.commit()


if __name__ == "__main__":
    db = Database("presets.db")
    print(db.selectPreset("test_no_drag"))
    print(db.selectRecord("*", "Presets", {"EID": 1}))
