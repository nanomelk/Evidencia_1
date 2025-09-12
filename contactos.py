import tkinter as tk
from tkinter import ttk


class Contactos:
    def __init__(self):
        # Ventana raíz
        self.root = tk.Tk()
        self.root.title("Contactos")
        self.root.geometry("700x450")

        # Hacer que la celda (0,0) de root se expanda
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Frame principal colocado con grid
        self.main = tk.Frame(self.root, padx=10, pady=10)
        self.main.grid(row=0, column=0, sticky="nsew")

        # Configurar rejilla del frame principal
        # 0=formulario, 1=botonera, 2=tabla
        self.main.rowconfigure(0, weight=0)
        self.main.rowconfigure(1, weight=0)
        self.main.rowconfigure(2, weight=1)  # la tabla crece
        self.main.columnconfigure(0, weight=1)

        self._build_ui()

    def _build_ui(self):
        # ===== Formulario (fila 0) =====
        form = tk.Frame(self.main)
        form.grid(row=0, column=0, sticky="ew")
        # columnas del formulario: 0=label, 1=entry
        form.columnconfigure(0, weight=0)
        form.columnconfigure(1, weight=1)

        tk.Label(form, text="Nombre").grid(
            row=0, column=0, sticky="w", padx=(0, 8), pady=4
        )
        self.ent_nombre = tk.Entry(form)
        self.ent_nombre.grid(row=0, column=1, sticky="ew", pady=4)

        tk.Label(form, text="Apellido").grid(
            row=1, column=0, sticky="w", padx=(0, 8), pady=4
        )
        self.ent_apellido = tk.Entry(form)
        self.ent_apellido.grid(row=1, column=1, sticky="ew", pady=4)

        tk.Label(form, text="Teléfono").grid(
            row=2, column=0, sticky="w", padx=(0, 8), pady=4
        )
        self.ent_telefono = tk.Entry(form)
        self.ent_telefono.grid(row=2, column=1, sticky="ew", pady=4)

        tk.Label(form, text="Email").grid(
            row=3, column=0, sticky="w", padx=(0, 8), pady=4
        )
        self.ent_email = tk.Entry(form)
        self.ent_email.grid(row=3, column=1, sticky="ew", pady=4)

        # ===== Botonera (fila 1) =====
        btns = tk.Frame(self.main)
        btns.grid(row=1, column=0, sticky="ew", pady=(6, 8))
        # repartir espacio entre botones
        for i in range(4):
            btns.columnconfigure(i, weight=1)

        tk.Button(btns, text="Agregar", command=self.agregar_datos).grid(
            row=0, column=0, padx=4, sticky="ew"
        )
        tk.Button(btns, text="Actualizar", command=self.actualizar).grid(
            row=0, column=1, padx=4, sticky="ew"
        )
        tk.Button(btns, text="Eliminar", command=self.eliminar).grid(
            row=0, column=2, padx=4, sticky="ew"
        )
        tk.Button(btns, text="Listar", command=self.cargar_tabla).grid(
            row=0, column=3, padx=4, sticky="ew"
        )

        # ===== Tabla (fila 2) =====
        tabla_frame = tk.Frame(self.main)
        tabla_frame.grid(row=2, column=0, sticky="nsew")
        tabla_frame.rowconfigure(0, weight=1)
        tabla_frame.columnconfigure(0, weight=1)

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=("id", "nombre", "apellido", "telefono", "email"),
            show="headings",
        )
        for col, txt in zip(
            self.tabla["columns"], ("ID", "Nombre", "Apellido", "Teléfono", "Email")
        ):
            self.tabla.heading(col, text=txt)
            self.tabla.column(col, anchor="w", width=120)
        self.tabla.grid(row=0, column=0, sticky="nsew")

        # Barra de scroll
        vsb = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky="ns")

    # ==== Callbacks de ejemplo ====
    def agregar_datos(self):
        # acá iría tu lógica de inserción en DB
        print(
            "Agregar:",
            self.ent_nombre.get(),
            self.ent_apellido.get(),
            self.ent_telefono.get(),
            self.ent_email.get(),
        )

    def actualizar(self):
        print("Actualizar seleccionado")

    def eliminar(self):
        print("Eliminar seleccionado")

    def cargar_tabla(self):
        # ejemplo: limpiar y cargar filas dummy
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        data_demo = [
            (1, "Ana", "Pérez", "351-123", "ana@example.com"),
            (2, "Luis", "Gómez", "351-456", "luis@example.com"),
        ]
        for fila in data_demo:
            self.tabla.insert("", "end", values=fila)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Contactos().run()
