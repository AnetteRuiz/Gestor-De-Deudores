from flask import Flask, render_template, request, redirect, url_for
import openpyxl.workbook
import pymysql, openpyxl,uuid

app = Flask(__name__)

@app.route("/")
def index():
    status = request.args.get('status')
    return render_template("index.html", status=status)

@app.route("/add_deudor", methods=['POST'])
def add_deudor():
    if request.method == 'POST':
        nombre = request.form['nombre'].lower()
        paterno = request.form['paterno'].lower()
        materno = request.form['materno'].lower()
        apodo = request.form['apodo'].lower()
        telefono = request.form['telefono']


        try:
            conexion = pymysql.connect(user='root', password='12345', host='localhost', database='deudores', port=3306)
            cursor = conexion.cursor()

            # Ejecuta la consulta para agregar al deudor
            cursor.execute("INSERT INTO deudores (nombre, paterno, materno, apodo, telefono) VALUES (%s, %s, %s, %s, %s)", 
                           (nombre, paterno, materno, apodo, telefono))
            conexion.commit()

            # Obtiene el ID del deudor recién agregado
            cursor.execute("SELECT id FROM deudores WHERE apodo = %s", (apodo,))
            id_deudor = cursor.fetchone()[0]

            fechaInicio = request.form['fechaInicio']
            monto_total = request.form['monto_total']
            
            cursor.execute("INSERT INTO deuda (fechaInicio, monto_total, id_deudor) VALUES (%s, %s, %s)", 
                           (fechaInicio, monto_total, id_deudor))
            conexion.commit()

            return redirect(url_for('index', status="success"))
        except pymysql.MySQLError as e:
            print(e)
            return redirect(url_for('index', status="error"))
        finally:
            if conexion:
                conexion.close()

@app.route("/Eliminar_deudor", methods=['POST'])
def eliminar_deudor():
      if request.method == 'POST':
        delete_method = request.form['delete_method']
        apodo = request.form.get('apodo').lower()
        nombre = request.form.get('nombre').lower()
        apellido_paterno = request.form.get('paterno').lower()
        apellido_materno = request.form.get('materno').lower()

        try:
            conexion = pymysql.connect(user='root', password='12345', host='localhost', database='deudores', port=3306)
            cursor = conexion.cursor()

            if delete_method == "apodo" and apodo:
                cursor.execute("SELECT id FROM deudores WHERE apodo = %s", (apodo,))
                id_deudor = cursor.fetchone()[0]
                
                cursor.execute("SELECT id FROM deuda WHERE id_deudor = %s", (id_deudor,))
                id_deuda = cursor.fetchone()[0]

                cursor.execute("DELETE FROM abono WHERE id_deuda = %s", (id_deuda,))
                
                cursor.execute("Delete from deuda where id_deudor = %s", (id_deudor,))
                
                cursor.execute("DELETE FROM deudores WHERE apodo = %s", (apodo,))
                
            elif delete_method == "nombre" and apellido_paterno and apellido_materno :
                print(nombre)
                print(apellido_paterno)
                print(apellido_materno)
                cursor.execute("SELECT id FROM deudores WHERE nombre = %s and paterno = %s and materno = %s", (nombre, apellido_paterno, apellido_materno))
                id_deudor = cursor.fetchone()[0]
                
                cursor.execute("SELECT id FROM deuda WHERE id_deudor = %s", (id_deudor,))
                id_deuda = cursor.fetchone()[0]

                cursor.execute("DELETE FROM abono WHERE id_deuda = %s", (id_deuda,))

                cursor.execute("Delete from deuda where id_deudor = %s", (id_deudor,))
                
                cursor.execute("DELETE FROM deudores WHERE nombre = %s AND paterno = %s AND materno = %s",
                            (nombre, apellido_paterno, apellido_materno))
            conexion.commit()

            return redirect(url_for('index', status="success"))
        except pymysql.MySQLError as e:
            print(e)
            return redirect(url_for('index', status="error"))
        finally:
            if conexion:
                conexion.close()

@app.route("/Abono", methods=['POST'])
def agregar_Abono():
    if request.method == 'POST':
        update_method = request.form['update_method']
        apodo = request.form.get('apodo').lower()
        nombre = request.form.get('nombre').lower()
        apellido_paterno = request.form.get('paterno').lower()
        apellido_materno = request.form.get('materno').lower()
        fechaRegistro = request.form.get('fechaRegistro')
        monto_abono = request.form.get('monto_abono')

        print(apodo)
        try:
            conexion = pymysql.connect(user='root', password='12345', host='localhost', database='deudores', port=3306)
            cursor = conexion.cursor()

            if update_method == "apodo" and apodo:

                cursor.execute("SELECT id FROM deudores WHERE apodo = %s", (apodo,))
                id_deudor = cursor.fetchone()[0]
                print (id_deudor)

                cursor.execute("SELECT id FROM deuda WHERE id_deudor = %s", (id_deudor,))
                id_deuda = cursor.fetchone()[0]
                print (id_deuda)

                cursor.execute("SELECT monto_total FROM deuda WHERE id_deudor = %s", (id_deudor,))
                monto_total = cursor.fetchone()[0]
               

                cursor.execute("CALL spAbono(%s, %s, %s);", 
                           (monto_total,monto_abono,id_deuda))
                conexion.commit()

                cursor.execute("INSERT INTO abono (fechaRegistro, monto_abono, id_deuda) VALUES (%s, %s, %s)", 
                           (fechaRegistro, monto_abono, id_deuda))
                conexion.commit()

    
                
            elif update_method == "nombre" and apellido_paterno and apellido_materno :
        
                cursor.execute("SELECT id FROM deudores WHERE nombre = %s and paterno = %s and materno = %s", (nombre, apellido_paterno, apellido_materno))
                id_deudor = cursor.fetchone()[0]
            

                cursor.execute("SELECT id FROM deuda WHERE id_deudor = %s", (id_deudor,))
                id_deuda = cursor.fetchone()[0]
              

                cursor.execute("SELECT monto_total FROM deuda WHERE id_deudor = %s", (id_deudor,))
                monto_total = cursor.fetchone()[0]
               

                cursor.execute("CALL spAbono(%s, %s, %s);", 
                           (monto_total,monto_abono,id_deuda))
                conexion.commit()

                cursor.execute("INSERT INTO abono (fechaRegistro, monto_abono, id_deuda) VALUES (%s, %s, %s)", 
                           (fechaRegistro, monto_abono, id_deuda))
                conexion.commit()

            conexion.commit()

            return redirect(url_for('index', status="success"))
        except pymysql.MySQLError as e:
            print(e)
            return redirect(url_for('index', status="error"))
        finally:
            if conexion:
                conexion.close()

@app.route("/Abonos", methods=['POST'])
def descarga_abonos():
      

        try:
            conexion = pymysql.connect(user='root', password='12345', host='localhost', database='deudores', port=3306)
            cursor = conexion.cursor()

            abonos = []

            cursor.execute("select * from vwdatos_abono")
            result = cursor.fetchall()
            for row in result:
                abonos.append(row)
            

            conexion.commit()
            print(abonos)

            excel_book = openpyxl.Workbook()
            sheet = excel_book.active

            sheet ['A1'] = "Nombre"
            sheet ['B1'] = "Paterno"
            sheet ['C1'] = "Materno"
            sheet ['D1'] = "Apodo"
            sheet ['E1'] = "Telefono"
            sheet ['F1'] = "Fecha_Registro"
            sheet ['G1'] = "Abono"

            for index, row in enumerate(abonos):
                sheet [f'A{index+2}'] = row[0]
                sheet [f'B{index+2}'] = row[1]
                sheet [f'C{index+2}'] = row[2]
                sheet [f'D{index+2}'] = row[3]
                sheet [f'E{index+2}'] = row[4]
                sheet [f'F{index+2}'] = row[5]
                sheet [f'G{index+2}'] = row[6]

            excel_book.save("excel_abonos.xlsx")


            return abonos
        except pymysql.MySQLError as e:
            print(e)
        finally:
            if conexion:
                conexion.close()

@app.route("/Deudas", methods=['POST'])
def descarga_deudas():
      

        try:
            conexion = pymysql.connect(user='root', password='12345', host='localhost', database='deudores', port=3306)
            cursor = conexion.cursor()

            deudas = []

            cursor.execute("select * from vwdatos_deuda")
            result = cursor.fetchall()
            for row in result:
                deudas.append(row)
            

            conexion.commit()
            print(deudas)

            excel_book = openpyxl.Workbook()
            sheet = excel_book.active

            sheet ['A1'] = "Nombre"
            sheet ['B1'] = "Paterno"
            sheet ['C1'] = "Materno"
            sheet ['D1'] = "Apodo"
            sheet ['E1'] = "Telefono"
            sheet ['F1'] = "Fecha_Inicio"
            sheet ['G1'] = "Fecha_Final"
            sheet ['H1'] = "Monto_total"

            for index, row in enumerate(deudas):
                sheet [f'A{index+2}'] = row[0]
                sheet [f'B{index+2}'] = row[1]
                sheet [f'C{index+2}'] = row[2]
                sheet [f'D{index+2}'] = row[3]
                sheet [f'E{index+2}'] = row[4]
                sheet [f'F{index+2}'] = row[5]
                sheet [f'G{index+2}'] = row[6]
                sheet [f'H{index+2}'] = row[7]

            excel_book.save("excel_deudas.xlsx")


            return deudas
        except pymysql.MySQLError as e:
            print("Error al eliminar deudor:", e)
        finally:
            if conexion:
                conexion.close()

if __name__ == '__main__':
    app.run(debug=True)
