import tkinter as tk
from tkinter import ttk, messagebox
from contacto_db import ContactoDB

class Contactos:
    def __init__(self):
        self.db = ContactoDB("Contactos.db")
        self.root = tk.Tk()
        self.root.title("Contactos")
        self.root.geometry("700x450")

        # expandir
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.main = tk.Frame(self.root, padx=10, pady=10)
        self.main.grid(row=0, column=0, sticky="nsew")

        self.main.rowconfigure(0, weight=0)
        self.main.rowconfigure(1, weight=0)
        self.main.rowconfigure(2, weight=1)
        self.main.columnconfigure(0, weight=1)

        self.selected_id = None  # <- guardamos el id seleccionado
        self._build_ui()
        self.cargar_tabla()

    def _build_ui(self):
        # ===== Formulario
        form = tk.Frame(self.main)
        form.grid(row=0, column=0, sticky="ew")
        form.columnconfigure(0, weight=0)
        form.columnconfigure(1, weight=1)

        tk.Label(form, text="Nombre").grid(row=0, column=0, sticky="w", padx=(0,8), pady=4)
        self.ent_nombre = tk.Entry(form); self.ent_nombre.grid(row=0, column=1, sticky="ew", pady=4)

        tk.Label(form, text="Apellido").grid(row=1, column=0, sticky="w", padx=(0,8), pady=4)
        self.ent_apellido = tk.Entry(form); self.ent_apellido.grid(row=1, column=1, sticky="ew", pady=4)

        tk.Label(form, text="Teléfono").grid(row=2, column=0, sticky="w", padx=(0,8), pady=4)
        self.ent_telefono = tk.Entry(form); self.ent_telefono.grid(row=2, column=1, sticky="ew", pady=4)

        tk.Label(form, text="Email").grid(row=3, column=0, sticky="w", padx=(0,8), pady=4)
        self.ent_email = tk.Entry(form); self.ent_email.grid(row=3, column=1, sticky="ew", pady=4)

        # ===== Botonera
        btns = tk.Frame(self.main)
        btns.grid(row=1, column=0, sticky="ew", pady=(6,8))
        for i in range(4): btns.columnconfigure(i, weight=1)

        tk.Button(btns, text="Agregar",   command=self.agregar_datos).grid(row=0, column=0, padx=4, sticky="ew")
        tk.Button(btns, text="Actualizar", command=self.actualizar).grid(row=0, column=1, padx=4, sticky="ew")
        tk.Button(btns, text="Eliminar",   command=self.eliminar).grid(row=0, column=2, padx=4, sticky="ew")
        tk.Button(btns, text="Listar",     command=self.cargar_tabla).grid(row=0, column=3, padx=4, sticky="ew")

        # ===== Tabla
        tabla_frame = tk.Frame(self.main)
        tabla_frame.grid(row=2, column=0, sticky="nsew")
        tabla_frame.rowconfigure(0, weight=1)
        tabla_frame.columnconfigure(0, weight=1)

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=("id","nombre","apellido","telefono","email"),
            show="headings", selectmode="browse"
        )
        for col, txt in zip(self.tabla["columns"], ("ID","Nombre","Apellido","Teléfono","Email")):
            self.tabla.heading(col, text=txt)
            self.tabla.column(col, anchor="w", width=120)
        self.tabla.grid(row=0, column=0, sticky="nsew")

        vsb = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky="ns")

        # Selección: al seleccionar una fila, cargo el form y guardo el id
        self.tabla.bind("<<TreeviewSelect>>", self._on_select)

    # ===== Helpers
    def _limpiar_form(self):
        for e in (self.ent_nombre, self.ent_apellido, self.ent_telefono, self.ent_email):
            e.delete(0, tk.END)

    def _get_form(self):
        return (self.ent_nombre.get().strip(),
                self.ent_apellido.get().strip(),
                self.ent_telefono.get().strip(),
                self.ent_email.get().strip())

    # ===== Eventos
    def _on_select(self, _evt=None):
        sel = self.tabla.selection()
        if not sel: return
        valores = self.tabla.item(sel[0], "values")  # (id, nombre, apellido, telefono, email)
        self.selected_id = valores[0]
        self._limpiar_form()
        self.ent_nombre.insert(0, valores[1])
        self.ent_apellido.insert(0, valores[2])
        self.ent_telefono.insert(0, valores[3])
        self.ent_email.insert(0, valores[4])

    # ===== Acciones
    def agregar_datos(self):
        nombre, apellido, telefono, email = self._get_form()
        if not nombre or not apellido:
            messagebox.showwarning("Atención", "Nombre y Apellido son obligatorios.")
            return
        self.db.agregar(nombre, apellido, telefono, email)
        self.cargar_tabla()
        self._limpiar_form()
        self.selected_id = None
        messagebox.showinfo("Éxito", "Contacto agregado.")

    def actualizar(self):
        if not self.selected_id:
            messagebox.showinfo("Info", "Seleccioná un contacto de la tabla.")
            return
        nombre, apellido, telefono, email = self._get_form()
        if not nombre or not apellido:
            messagebox.showwarning("Atención", "Nombre y Apellido son obligatorios.")
            return
        self.db.actualizar(self.selected_id, nombre, apellido, telefono, email)
        self.cargar_tabla()
        messagebox.showinfo("Éxito", "Contacto actualizado.")

    def eliminar(self):
        if not self.selected_id:
            messagebox.showinfo("Info", "Seleccioná un contacto de la tabla.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar el contacto seleccionado?"):
            self.db.eliminar(self.selected_id)
            self.cargar_tabla()
            self._limpiar_form()
            self.selected_id = None

    def cargar_tabla(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        for fila in self.db.listar():
            self.tabla.insert("", "end", values=fila)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    Contactos().run()
