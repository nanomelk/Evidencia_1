import sqlite3

class ContactoDB:
    def __init__(self, archivo="Contactos.db"):
        self.conn = sqlite3.connect(archivo)
        self.cur = self.conn.cursor()
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS contactos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT,
            email TEXT
        )""")
        self.conn.commit()

    def agregar(self, nombre, apellido, telefono, email):
        self.cur.execute("INSERT INTO contactos (nombre, apellido, telefono, email) VALUES (?, ?, ?, ?)",
                         (nombre, apellido, telefono, email))
        self.conn.commit()

    def listar(self):
        self.cur.execute("SELECT * FROM contactos")
        return self.cur.fetchall()

    def actualizar(self, contacto_id, nombre, apellido, telefono, email):
        self.cur.execute("""
        UPDATE contactos
        SET nombre=?, apellido=?, telefono=?, email=?
        WHERE id=?
        """, (nombre, apellido, telefono, email, contacto_id))
        self.conn.commit()

    def eliminar(self, contacto_id):
        self.cur.execute("DELETE FROM contactos WHERE id=?", (contacto_id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
