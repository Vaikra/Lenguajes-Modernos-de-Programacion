from flask import Flask, render_template, request, redirect, url_for
import MySQLdb

app = Flask(__name__)

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'salazar25'
app.config['MYSQL_DB'] = 'flask_db'

def get_db_connection():
    """Crea una nueva conexión a la base de datos."""
    return MySQLdb.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        passwd=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB']
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', usuarios=data)

@app.route('/add', methods=['POST'])
def add_usuario():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        
        # Validación básica
        if not nombre or not apellido:
            return "Nombre y apellido son requeridos", 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (nombre, apellido) VALUES (%s, %s)", (nombre, apellido))
            conn.commit()
        except Exception as e:
            conn.rollback()
            return f"Error al agregar usuario: {e}", 500
        finally:
            cursor.close()
            conn.close()
        
        return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return f"Error al eliminar usuario: {e}", 500
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        
        # Validación básica
        if not nombre or not apellido:
            return "Nombre y apellido son requeridos", 400
        
        try:
            cursor.execute("UPDATE usuarios SET nombre = %s, apellido = %s WHERE id = %s", (nombre, apellido, id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            return f"Error al actualizar usuario: {e}", 500
        finally:
            cursor.close()
            conn.close()
        
        return redirect(url_for('index'))
    
    # Si es GET, mostramos el formulario de edición
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if usuario is None:
        return "Usuario no encontrado", 404
    
    return render_template('edit.html', usuario=usuario)

@app.route('/select/<int:id>')
def select_usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if usuario is None:
        return "Usuario no encontrado", 404
    
    return render_template('select.html', usuario=usuario)

if __name__ == '__main__':
    app.run(debug=True)
