from flask import Flask, render_template, request, redirect
import MySQLdb

app = Flask(__name__)

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'salazar25'
app.config['MYSQL_DB'] = 'flask_db'

# Conectar a la base de datos MySQL
db = MySQLdb.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    passwd=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)

# Crear cursor para ejecutar las consultas
cursor = db.cursor()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM usuarios")
    data = cursor.fetchall()
    return render_template('index.html', usuarios=data)

@app.route('/add', methods=['POST'])
def add_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        cursor.execute("INSERT INTO usuarios (nombre, apellido) VALUES (%s, %s)", (nombre, apellido))
        db.commit()
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
