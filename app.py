import os
from flask import Flask
from flask import render_template, request, redirect, session, url_for
from flask import send_from_directory
from sqlalchemy import create_engine
import pandas as pd
import pymysql
import numpy as np
#from flaskext.mysql import MySQL

app = Flask(__name__)
conn = pymysql.connect(host='34.27.5.115',
                             user='root',
                             password='Adm123!',
                             database='DWH',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()

'''
#--------------------------------------------
# Asignación de formato css
#--------------------------------------------
@app.route('/css/<archivocss>')
def css_link(archivocss):
    return send_from_directory( os.path.join('templates/sitio/css'), archivocss)

@app.route('/imag/<imagen>')
def imagenes(imagen):
    return send_from_directory( os.path.join('templates/sitio/img'), imagen)

'''   
#--------------------------------------------
# Link a las pestañas
#--------------------------------------------

@app.route('/')
def inicio():
    return render_template( 'sitio/index.html')

@app.route('/productos')
def productos():
    return render_template( 'sitio/productos.html')

'''
@app.route('/cheklogin',method = ['POST'])
def checklogin():
    return render_template( 'sitio/checklogin.html')
'''

@app.route('/nosotros')
def nosotros():
    return render_template( 'sitio/nosotros.html')


@app.route('/Login-Registro')
def login_registro():
    return render_template( 'sitio/login_registro.html')

@app.route('/sesion')
def sesion():
    return render_template( 'sitio/sesion.html')


@app.route('/admin/')
def admin_index():
    return render_template( 'admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template( 'admin/login.html')

@app.route('/admin/productos')
def admin_productos():
    sql = "SELECT * FROM DSA.PRODUCTOS_PRUEBA"
    cursor.execute(sql)
    productos = cursor.fetchall()
    conn.commit()
    print(productos)
    return render_template( '/admin/productos.html', productos = productos)

@app.route('/admin/productos/guardar', methods = ['POST'])
def submit_form():
    # Recuperar datos del formulario
    _nombre = request.form['txtNombre']
    _url = request.form['txtURL']
    _archivo = request.files['txtImagen']
    # Ejecutar consulta SQL para insertar datos en la base de datos
    sql = "INSERT INTO DSA.PRODUCTOS_PRUEBA(NOMBRE, IMAGEN, URL)  VALUES (%s, %s, %s )"
    cursor.execute(sql, (_nombre,_archivo.filename, _url))
    conn.commit()

    return redirect('/admin/productos')

@app.route('/sitio/login_registro/guardar', methods = ['POST'])
def submit_registro():
    # Recuperar datos del formulario
    _nombre_completo = request.form['nombre_completo']
    _correo_electronico= request.form['correo']
    _usuario = request.form['usuario']
    _contrasenia = request.form['contrasena']
    # Ejecutar consulta SQL para insertar datos en la base de datos
    sql = "INSERT INTO DSA.REGISTRO(ID,NOMBRE_COMPLETO, CORREO_ELECTRONICO, USUARIO, CONTRASENIA) VALUES (null, %s, %s, %s, %s )"
    cursor.execute(sql, ( _nombre_completo,_correo_electronico, _usuario, _contrasenia  ))
    conn.commit()
    return redirect('/Login-Registro')

# Funcion Login Final
@app.route('/sitio/acceso-login', methods = ['GET','POST'])
def login():
    if request.method == 'POST' and 'ingrese_correo' in request.form and 'ingrese_contraseña':
        correo_ = request.form['ingrese_correo']
        password_ = request.form['ingrese_contraseña']
        # Ejecuta la instrucción para ver si existe el correo
        sql = "SELECT * FROM DSA.REGISTRO WHERE CORREO_ELECTRONICO = %s and CONTRASENIA = %s"
        cursor.execute(sql, ( correo_, password_, ))
        account = cursor.fetchone()
        if account:
            session['nombre_completo'] = account['NOMBRE_COMPLETO']
            session['correo'] = correo_
            session['logueado'] = True
            session['ID'] = account['ID']
            return redirect('/sesion')
        else:
            return render_template('/sitio/login_registro.html', mensaje = "Usuario o contraseña incorrecta") 
            
        
@app.route('/logout')
def logout():
    session.clear() 
    return redirect('/Login-Registro')




if __name__ == "__main__":
    app.secret_key = "Nandomh123"
    app.run( debug = True )