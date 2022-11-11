from flask import Flask, render_template, request
import mysql.connector
#from flask_mysqldb import MySql

app = Flask(__name__)

# app.config['MYSQL_HOST'] =  'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] =  'coltis_flask'
# app.config['MYSQL_PORT'] =  3306
# mysql = MySQL(app)

def conectar():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="coltis_flask",
        port=3306
    )
    return db

@app.route("/")
def saludo():
    return render_template("index.html")

@app.route("/admin/estudiantes")
def estudiantes(datos = dict()):
    try:
      sql = """
            SELECT codigo, nombres, apellidos, correo, telefono
            FROM estudiante
            """
      db = conectar()
      cursor = db.cursor()
      cursor.execute(sql)
      datos["estudiantes"] = cursor.fetchall()
      db.close()

    except:
        datos["error"]="Error al consultar los estudiantes"

    return render_template("estudiantes.html", modelo = datos)

@app.route("/admin/estudiantes/nuevo", methods = ["POST"])
def nuevo_estudiante():
    codigo = request.form["codigo"]
    nombre = request.form["nombres"]
    apellido = request.form["apellidos"]
    correo = request.form["correo"]
    telefono = request.form["telefono"]

    datos = dict()
    try:
      sql = f"""
                INSERT INTO estudiante (codigo, nombres, apellidos, correo, telefono)
                VALUES ('{codigo}','{nombre}','{apellido}','{correo}','{telefono}');
            """
      db = conectar()
      cursor = db.cursor()
      cursor.execute(sql)
      filas = cursor.rowcount
      db.commit()
      db.close()
      if filas != 1:
            datos["error"] = "Numero de filas afectadas no es correcto"

    except:
        datos["error"] = "Error al insertar los datos del estudiante."

    return estudiantes(datos)

@app.route("/admin/estudiantes/editar/<id>")
def editar(id: str):
    datos = dict()
    try:
        if id == None or len(id) == 0:
            raise Exception("El codigo no puede estar vacio")
        
        # Consultar la informacion del estudiante con codigo = id
        sql = f"""
            SELECT codigo, nombres, apellidos, correo, telefono
            FROM estudiante
            WHERE codigo = '{id}'
            """
        db = conectar()
        cursor = db.cursor()
        cursor.execute(sql)
        # Cargar la informacion del estudiante en la plantilla
        datos["estudiante"] = cursor.fetchone()
        print(datos)
        db.close()

        # Mostrar la plantilla
        return render_template("estudiantes_editar.html", modelo = datos)
    except Exception as ex:
        datos["error"] = str(ex)
        return estudiantes(datos)    
    
    
@app.route("/admin/estudiantes/actualizar", methods = ["POST"])
def actualizar_estudiante():
    codigo = request.form["codigo"]
    nombre = request.form["nombres"]
    apellido = request.form["apellidos"]
    correo = request.form["correo"]
    telefono = request.form["telefono"]

    datos = dict()
    try:
        sql = f"""
                UPDATE estudiante
                SET nombres = '{nombre}',
                    apellidos = '{apellido}',
                    correo = '{correo}',
                    telefono = '{telefono}'
                WHERE codigo = '{codigo}';
            """
        db = conectar()
        cursor = db.cursor()
        cursor.execute(sql)
        filas = cursor.rowcount
        db.commit()
        db.close()
        if filas != 1:
            datos["error"] = "Numero de filas afectadas no es correcto"
        else:
            datos["exito"] = f"Estudiante '{nombre} {apellido}' fue actualizado exitosamente"

    except:
        datos["error"] = "Error al actualizar los datos del estudiante."

    return estudiantes(datos)
    
    
@app.route("/admin/estudiantes/eliminar/<id>")
def eliminar(id: str):
    datos = dict()
    try:
        if id == None or len(id) == 0:
            raise Exception("El codigo no puede estar vacio")
        
        # Consultar la informacion del estudiante con codigo = id
        sql = f"""
            DELETE
            FROM estudiante
            WHERE codigo = '{id}'
            """
        db = conectar()
        cursor = db.cursor()
        cursor.execute(sql)
        filas = cursor.rowcount
        db.commit()
        db.close()
        if filas != 1:
            datos["error"] = "Numero de filas afectadas no es correcto"
        else:
            datos["exito"] = f"Estudiante fue eliminado exitosamente"
    except Exception as ex:
        datos["error"] = str(ex)
        
    return estudiantes(datos)






    
@app.route("/admin/materias")
def materias():
    return render_template("materias.html")



@app.route("/matriculas")
def matriculas():
    return render_template("matriculas.html")

@app.route("/matriculas/buscar", methods=["POST"])
def matriculas_buscar(codigo = None, datos = dict()):
    if codigo is None:
        codigo = request.form["codigo"]

    try:
        # Consultar datos de estudiante
        sql = f"""
            SELECT codigo, nombres, apellidos, correo, telefono
            FROM estudiante
            WHERE codigo = '{codigo}'
            """
        db = conectar()
        cursor = db.cursor()
        cursor.execute(sql)
        # Cargar la informacion del estudiante en la plantilla
        datos["estudiante"] = cursor.fetchone()
        db.close()

        # Consultar las materias del estudiante
        sql = f"""
            SELECT ma.id, ma.nombre, ma.creditos
            FROM matricula m
            JOIN materia ma on (m.id_materia = ma.id)
            WHERE m.codigo = '{codigo}'
            """
        db = conectar()
        cursor = db.cursor()
        cursor.execute(sql)
        # Cargar la informacion del estudiante en la plantilla
        datos["materias_estudiante"] = cursor.fetchall()
        db.close()

        # Consultar todas las materias del sistema
        sql = f"""
            SELECT id, nombre, creditos
            FROM materia
            ORDER BY nombre
            """
        db = conectar()
        cursor = db.cursor()
        cursor.execute(sql)
        # Cargar la informacion del estudiante en la plantilla
        datos["materias"] = cursor.fetchall()
        db.close()

    except:
        datos["error"] = "No se pudo cargar la informacion del usuario"

    # Enviar la informacion al formulario
    return render_template("matriculas.html", modelo = datos)


@app.route("/matriculas/agregar", methods=["POST"])
def agregar_matricula():
    codigo = request.form["codigo"]
    materia = request.form["materia"]

    datos = dict()
    try:
        sql = f"""
                INSERT INTO matricula (codigo, id_materia)
                VALUES ('{codigo}', {materia});
            """
        db = conectar()
        cursor = db.cursor()
        cursor.execute(sql)
        filas = cursor.rowcount
        db.commit()
        db.close()
        if filas != 1:
            datos["error"] = "Numero de filas afectadas no es correcto"
        else:
            datos["exito"] = f"Materia fue registrada exitosamente"

    except Exception as ex:
        datos["error"] = "Error al insertar la matricula del estudiante."
        print(ex)

    return matriculas_buscar(codigo, datos)


@app.route("/matriculas/eliminar/<codigo>/<materia>")
def eliminar_matricula(codigo, materia):
    datos = dict()
    try:
        if codigo == None or len(codigo) == 0:
            raise Exception("El codigo no puede estar vacio")
        
        # Consultar la informacion del estudiante con codigo = id
        sql = f"""
            DELETE
            FROM matricula
            WHERE codigo = '{codigo}'
            AND id_materia = {materia}
            """
        db = conectar()
        cursor = db.cursor()
        cursor.execute(sql)
        filas = cursor.rowcount
        db.commit()
        db.close()
        if filas != 1:
            datos["error"] = "Numero de filas afectadas no es correcto"
        else:
            datos["exito"] = f"Matricula eliminada exitosamente"
    except Exception as ex:
        datos["error"] = str(ex)
        
    return matriculas_buscar(codigo, datos)







app.run(debug=True)