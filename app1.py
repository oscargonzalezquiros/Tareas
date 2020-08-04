### ===========================================
### PROYECTO FINAL......: PYHTON
### METODOS.............: GET-PUT-POST-DELETE
### ALUMNO..............: OSCAR GONZALEZ QUIROS
### ============================================

from flask import Flask, jsonify, request, json
from flask_cors import CORS
import mysql.connector

### ===================
### METODO VALIDAR PING
### ===================


app = Flask(__name__)

CORS(app)

### =============================================
### mydb se define el conector a la base de datos
### ==============================================

mydb = mysql.connector.connect(
    host='localhost',  # ip remote
    user='root',
    password='111265'
)

### =============================================
### Si no existe la base de dat se crea
### ==============================================

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS Oscar")

mycursor.execute("USE Oscar")

mycursor.execute("""CREATE TABLE IF NOT EXISTS tareas (
    id INT AUTO_INCREMENT PRIMARY KEY, descripcion VARCHAR(150),
    fecha timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, usuario CHAR(10),
    estado CHAR(1))""")

#mycursor.execute("TRUNCATE TABLE tareas")

#mycursor.execute("INSERT INTO tareas(descripcion, fecha, usuario, estado) values('first record', current_timestamp, 'ogonzalez', 'a')")

### ===============================
### Selecciona todas las tares
### ===============================

@app.route('/tareas')
def select_all_tareas():
    sql = 'SELECT id, descripcion, fecha, usuario, estado FROM tareas'
    try:
        mycursor.execute(sql)
        tareas = mycursor.fetchall()
        return jsonify({"tareas": tareas, "message": "Tareas's Records"})

    except Exception as e:
        raise

### ===============================
### Busqueda la Tarea
### ===============================

@app.route('/tarea/<string:id>')
def select_tarea(id):
    sql = "SELECT id, descripcion, fecha, usuario, estado FROM tareas WHERE id = '{}'".format(id)

    try:
        mycursor.execute(sql)
        tarea = mycursor.fetchone()
        return jsonify({"tarea": tarea})

    except Exception as e:
        raise

### ===============================
### Inserta nueva Tarea
### ===============================

@app.route('/tarea', methods=['POST'])
def addTarea():

    new_tarea = {
        "descripcion": request.json["descripcion"],
        "usuario": request.json["usuario"],
        "estado": request.json["estado"]
    }

    sql = "INSERT INTO tareas(descripcion, fecha, usuario, estado) values('{c[descripcion]}', current_timestamp, '{c[usuario]}', '{c[estado]}')".format(c=new_tarea)

    try:
        mycursor.execute(sql)
        mydb.commit()

        sql = 'SELECT max(id) FROM tareas'
        mycursor.execute(sql)
        id = mycursor.fetchone()
        sql = "SELECT id, descripcion, fecha, usuario, estado FROM tareas WHERE id = '{}'".format(id[0])
        mycursor.execute(sql)
        tarea = mycursor.fetchone()

        return jsonify({"message": "Se agrega tarea", "tarea": tarea})

    except Exception as e:
        raise


### ===============================
### Modifica la Tarea
### ===============================

@app.route('/tarea/u', methods=['PUT'])
def update_tarea():

    edit_tarea = {
        "id": request.json["id"],
        "descripcion": request.json["descripcion"],
        "usuario": request.json["usuario"],
        "estado": request.json["estado"]
    }

    sql = "UPDATE tareas SET descripcion='{c[descripcion]}', fecha = current_timestamp, usuario = '{c[usuario]}', estado = '{c[estado]}' WHERE id = '{c[id]}'".format(c=edit_tarea)

    try:
        mycursor.execute(sql)
        mydb.commit()

        sql = "SELECT id, descripcion, fecha, usuario, estado FROM tareas WHERE id = '{}'".format(id)
        mycursor.execute(sql)
        tarea = mycursor.fetchone()

        return jsonify({
            "message": "Se modifica la tarea",
            "tarea": tarea
        })

    except Exception as e:
        raise


@app.route('/tarea/<string:id>', methods=['DELETE'])
def deleteTarea(id):

    sql = "DELETE FROM tareas WHERE id = '{}'".format(id)

    try:
        mycursor.execute(sql)
        mydb.commit()

        return jsonify({"message": "Se elimina la Tarea"})

    except Exception as e:
        raise

### ===============================
### Finaliza el programa
### ===============================

if __name__  == '__main__':
   app.run(debug=True, port=5000)
