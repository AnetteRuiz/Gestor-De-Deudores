from flask import Flask, render_template, request, redirect, url_for
from models import Deudores

app = Flask(__name__)

# Instancia de la clase Deudores
db = Deudores(user="root", password="12345", host="localhost", database="deudores")

@app.route("/")
def index():
    status = request.args.get("status")
    return render_template("index.html", status=status)


@app.route("/add_deudor", methods=["POST"])
def add_deudor():
    try:
        db.add_deudor(
            nombre=request.form["nombre"].lower(),
            paterno=request.form["paterno"].lower(),
            materno=request.form["materno"].lower(),
            apodo=request.form["apodo"].lower(),
            telefono=request.form["telefono"],
            fecha_inicio=request.form["fechaInicio"],
            monto_total=request.form["monto_total"],
        )
        return redirect(url_for("index", status="success"))
    except Exception as e:
        print(e)
        return redirect(url_for("index", status="error"))


@app.route("/Eliminar_deudor", methods=["POST"])
def eliminar_deudor():
    try:
        delete_method = request.form["delete_method"]
        kwargs = {
            "apodo": request.form.get("apodo", "").lower(),
            "nombre": request.form.get("nombre", "").lower(),
            "paterno": request.form.get("paterno", "").lower(),
            "materno": request.form.get("materno", "").lower(),
        }
        db.delete_deudor(delete_method, **kwargs)
        return redirect(url_for("index", status="success"))
    except Exception as e:
        print(e)
        return redirect(url_for("index", status="error"))

@app.route("/Abono", methods=["POST"])
def agregar_Abono():
    try:
        db.agregar_abono(
            update_method=request.form["update_method"],
            apodo=request.form.get("apodo", "").lower(),
            nombre=request.form.get("nombre", "").lower(),
            paterno=request.form.get("paterno", "").lower(),
            materno=request.form.get("materno", "").lower(),
            fecha_registro=request.form.get("fechaRegistro"),
            monto_abono=request.form.get("monto_abono"),
        )
        return redirect(url_for("index", status="success"))
    except Exception as e:
        print(e)
        return redirect(url_for("index", status="error"))

@app.route("/Abonos", methods=["POST"])
def descarga_abonos():
    try:
        db.download_abonos()
        return redirect(url_for("index", status="success"))
    except Exception as e:
        print(e)
        return redirect(url_for("index", status="error"))


@app.route("/Deudas", methods=["POST"])
def descarga_deudas():
    try:
        db.download_deudas()
        return redirect(url_for("index", status="success"))
    except Exception as e:
        print(e)
        return redirect(url_for("index", status="error"))


if __name__ == "__main__":
    app.run(debug=True)
