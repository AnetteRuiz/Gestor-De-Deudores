import pymysql
import openpyxl


class Database:
    def __init__(self, user, password, host, database, port=3306):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.port = port

    def connect(self):
        return pymysql.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database,
            port=self.port
        )


class Deudores(Database):
    def add_deudor(self, nombre, paterno, materno, apodo, telefono, fecha_inicio, monto_total):
        try:
            conexion = self.connect()
            cursor = conexion.cursor()

            # Agregar deudor
            cursor.execute(
                "INSERT INTO deudores (nombre, paterno, materno, apodo, telefono) VALUES (%s, %s, %s, %s, %s)",
                (nombre, paterno, materno, apodo, telefono)
            )
            conexion.commit()

            cursor.execute("SELECT id FROM deudores WHERE apodo = %s", (apodo,))
            id_deudor = cursor.fetchone()[0]

            # Agregar deuda
            cursor.execute(
                "INSERT INTO deuda (fechaInicio, monto_total, id_deudor) VALUES (%s, %s, %s)",
                (fecha_inicio, monto_total, id_deudor)
            )
            conexion.commit()
        finally:
            conexion.close()

    def delete_deudor(self, delete_method, **kwargs):
        try:
            conexion = self.connect()
            cursor = conexion.cursor()

            if delete_method == "apodo":
                apodo = kwargs.get("apodo")
                cursor.execute("SELECT id FROM deudores WHERE apodo = %s", (apodo,))
                id_deudor = cursor.fetchone()[0]

            elif delete_method == "nombre":
                nombre, paterno, materno = kwargs.get("nombre"), kwargs.get("paterno"), kwargs.get("materno")
                cursor.execute(
                    "SELECT id FROM deudores WHERE nombre = %s AND paterno = %s AND materno = %s",
                    (nombre, paterno, materno)
                )
                id_deudor = cursor.fetchone()[0]

            cursor.execute("DELETE FROM abono WHERE id_deuda = (SELECT id FROM deuda WHERE id_deudor = %s)", (id_deudor,))
            cursor.execute("DELETE FROM deuda WHERE id_deudor = %s", (id_deudor,))
            cursor.execute("DELETE FROM deudores WHERE id = %s", (id_deudor,))
            conexion.commit()
        finally:
            conexion.close()

    def agregar_abono(self, update_method, apodo=None, nombre=None, paterno=None, materno=None, fecha_registro=None, monto_abono=None):
        try:
            conexion = self.connect()
            cursor = conexion.cursor()

            if update_method == "apodo" and apodo:
                # Obtener el ID del deudor y de la deuda usando el apodo
                cursor.execute("SELECT id FROM deudores WHERE apodo = %s", (apodo,))
                id_deudor = cursor.fetchone()[0]

                cursor.execute("SELECT id, monto_total FROM deuda WHERE id_deudor = %s", (id_deudor,))
                id_deuda, monto_total = cursor.fetchone()

            elif update_method == "nombre" and nombre and paterno and materno:
                # Obtener el ID del deudor y de la deuda usando nombre completo
                cursor.execute(
                    "SELECT id FROM deudores WHERE nombre = %s AND paterno = %s AND materno = %s",
                    (nombre, paterno, materno)
                )
                id_deudor = cursor.fetchone()[0]

                cursor.execute("SELECT id, monto_total FROM deuda WHERE id_deudor = %s", (id_deudor,))
                id_deuda, monto_total = cursor.fetchone()

            else:
                raise ValueError("Datos insuficientes para identificar al deudor.")

            # Llamar al procedimiento almacenado `spAbono`
            cursor.execute("CALL spAbono(%s, %s, %s);", (monto_total, monto_abono, id_deuda))
            conexion.commit()

            # Insertar registro en la tabla `abono`
            cursor.execute(
                "INSERT INTO abono (fechaRegistro, monto_abono, id_deuda) VALUES (%s, %s, %s)",
                (fecha_registro, monto_abono, id_deuda)
            )
            conexion.commit()
    
        finally:
            conexion.close()

    def download_abonos(self):
        try:
            conexion = self.connect()
            cursor = conexion.cursor()

            cursor.execute("SELECT * FROM vwdatos_abono")
            abonos = cursor.fetchall()

            excel_book = openpyxl.Workbook()
            sheet = excel_book.active
            sheet.append(["Nombre", "Paterno", "Materno", "Apodo", "Telefono", "Fecha_Registro", "Abono"])

            for row in abonos:
                sheet.append(row)

            excel_book.save("excel_abonos.xlsx")
        finally:
            conexion.close()

    def download_deudas(self):
        try:
            conexion = self.connect()
            cursor = conexion.cursor()

            cursor.execute("SELECT * FROM vwdatos_deuda")
            deudas = cursor.fetchall()

            excel_book = openpyxl.Workbook()
            sheet = excel_book.active
            sheet.append(["Nombre", "Paterno", "Materno", "Apodo", "Telefono", "Fecha_Inicio", "Fecha_Final", "Monto_total"])

            for row in deudas:
                sheet.append(row)

            excel_book.save("excel_deudas.xlsx")
        finally:
            conexion.close()
