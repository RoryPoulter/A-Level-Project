import sqlite3
from os import PathLike


class Database:
    def __init__(self, path):
        """
        :param path: Path to database file
        :type path: str | bytes | PathLike[str] | PathLike[bytes]
        """
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
        :type data: dict[str, Any]
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
        :type data: dict[str, Any]
        :return: The value in the field
        :rtype: list
        """
        fields = list(data.keys())
        values = list(data.values())
        q_marks = ", ".join(["?"] * len(data))
        self.c.execute(f"SELECT {field} FROM {table} WHERE ({", ".join(fields)}) IS ({q_marks})", values)
        return self.c.fetchall()

    def duplicateCheck(self, primary_field, table, data):
        """
        Checks for records in the table. If the record does not exist, the values are inserted into the table. Returns
        the primary key of the record with the specified values
        :param primary_field: The primary key of the table
        :type primary_field: str
        :param table: The name of the table
        :type table: str
        :param data: The data in the record
        :type data: dict[str, Any]
        :return: The primary key of the record
        """
        primary_key = self.selectRecord(primary_field, table, data)  # Selects the primary key from the record
        if not primary_key:  # If the record does not exist
            self.insertRecord(table, data)  # Inserts the record
            primary_key = self.selectRecord(primary_field, table, data)[0][0]  # Fetches the primary key of the record
        else:  # If the record exists
            primary_key = primary_key[0][0]  # Isolates the primary key from the record
        return primary_key

    def selectPreset(self, preset_name):
        """
        Fetches all the values in the preset from the different tables
        :param preset_name: The name of the preset
        :type preset_name: str
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
        Presets.name=?""", [preset_name])
        return self.c.fetchall()[0]

    def deleteRecord(self, table, field, primary_key):
        """
        Deletes a record from a table.
        :param table: The table which the record is being deleted from
        :type table: str
        :param field: The name of the primary field
        :type field: str
        :param primary_key: The primary key of the record to be deleted
        """
        self.c.execute(f"DELETE FROM {table} WHERE ({field}) IS ({primary_key})")
        self.db.commit()

    def getPresets(self):
        """
        Selects all the preset names
        :return: The preset names
        :rtype: list[str]
        """
        self.c.execute("SELECT name FROM Presets")
        records = self.c.fetchall()
        preset_names = list(zip(*records))[0]
        return list(preset_names)


if __name__ == "__main__":
    db = Database("presets.db")
    print(db.selectRecord("*", "Presets", {"EID": 1}))
    print(db.duplicateCheck("EID", "Environments", {"gravity": 9.81, "air_density": 1.2}))
    print(names := db.getPresets())
    for name in names:
        print(f"{name}: {db.selectPreset(name)}")
