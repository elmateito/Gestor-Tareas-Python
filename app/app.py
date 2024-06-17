from flask import Flask, render_template, request as req, redirect, url_for, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature
from flask_mail import Mail, Message
import matplotlib.pyplot as plt
import mysql.connector

app = Flask(__name__)
app.secret_key = '750'
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'task'
)

cursor = db.cursor()
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mat.se.arias@gmail.com'
app.config['MAIL_PASSWORD'] = 'jxck yoqf evxm qnbk'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = ('Servicio Nacional de Aprendizaje - CENIGRAF', 'mat.se.arias@gmail.com')

mail = Mail(app)

""" credenciales iniciar sesión:
    - usuario contraseña: usuario
    - admin contraseña: admin """

#iniciar sersión - de acuerdo al rol
@app.route('/', methods=['GET', 'POST'])
def logUsuario():
    if req.method == 'POST':
        nombreUsuario = req.form.get('nombreUsuario')
        contrasena = req.form.get('contrasena')
        cursor = db.cursor(dictionary=True)
        query = ('SELECT nombreUsuario, contraseña, rol FROM usuarios WHERE nombreUsuario = %s')
        cursor.execute(query,(nombreUsuario,))
        userData = cursor.fetchone()
        if userData and check_password_hash(userData['contraseña'], contrasena):
            session['nombreUsuario'] = userData['nombreUsuario']
            session['rol'] = userData['rol']
            if userData['rol'] == 'Administrador':
                return redirect(url_for('listarUsuarios'))
            else:
                return redirect(url_for('listarTareas'))
        else:
            print('Credenciales inválidas/erróneas')
            return render_template('index.html')
    return render_template('index.html')

#enviar correo - jxck yoqf evxm qnbk
def enviarCorreo(email):
    #generar token para el correo de recover
    token = serializer.dumps(email, salt='restablecerContrasena')
    enlace = url_for('restablecerContrasena', token=token, _external=True)
    mensaje = Message(subject='Restablecer Contraseña', recipients=[email], body=f'Llama la ficalia: :{enlace}')
    mail.send(mensaje)

#restablecer contraseña
@app.route('/restablecer-contrasena/<token>', methods=['GET', 'POST'])
def restablecerContrasena(token):
    try:
        email = serializer.loads(token, salt='restablecerContrasena', max_age=50000)
        if req.method == 'POST':
            nueva = req.form['contrasena']
            nueva2 = req.form['contrasena2']
            if nueva != nueva2:
                return print('Las contraseñas no coinciden')
            contrasena = generate_password_hash(nueva)
            cursor = db.cursor()
            cursor.execute("UPDATE usuarios SET contraseña = %s WHERE correo = %s", (contrasena, email))
            db.commit()
    except BadSignature:
        return print('Enlace expirado')
    return render_template('recuperarContrasena.html')

#olvidar-contraseña
@app.route("/olvidar-contrasena", methods=['GET', 'POST'])
def olvidarContrasena():
    if req.method == 'POST':
        email = req.form['email']
        enviarCorreo(email)
        return redirect(url_for('logUsuario'))
    return render_template('olvidarContrasena.html')

#registrar usuarios
@app.route('/registro-usuarios', methods=['GET', 'POST'])
def regUsuario():
    if req.method == 'POST':
        nombre = req.form.get('nombre')
        apellido = req.form.get('apellido')
        correo = req.form.get('correo')
        nombreUsuario = req.form.get('nombreUsuario')
        contrasena = req.form.get('contrasena')
        encriptar = generate_password_hash(contrasena)
        rol = req.form.get('rol')
        cursor = db.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE correo = %s AND nombreUsuario = %s', (correo, nombreUsuario))
        exist = cursor.fetchone()
        if exist:
            print('Usuario existente, inicie sesión')
            return render_template('regUsuarios.html')
        else:
            cursor.execute('INSERT INTO usuarios(nombre, apellido, correo, nombreUsuario, contraseña, rol) VALUES(%s, %s, %s, %s, %s, %s)',
                        (nombre, apellido, correo, nombreUsuario, encriptar, rol))
            db.commit()
            print('usuario registrado')
            return redirect(url_for('logUsuario'))
    return render_template('regUsuarios.html')

#listar usuarios
@app.route("/lista-usuarios", methods=['GET', 'POST'])
def listarUsuarios():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM usuarios')
    users = cursor.fetchall()
    return render_template('homeAdmin.html', users = users)

#eliminar usuarios
@app.route('/eliminar-usuario/<int:id>', methods=['GET'])
def delUsuario(id):
    cursor = db.cursor()
    cursor.execute('DELETE FROM usuarios WHERE idUsuario = %s', (id,))
    db.commit()
    return redirect(url_for('listarUsuarios'))

#buscar usuarios
@app.route('/buscar-usuarios', methods=['POST'])
def buscarUsuario():
    busqueda = req.form.get('busqueda')
    cursor = db.cursor(dictionary=True)
    consulta = 'SELECT * FROM usuarios WHERE idUsuario = %s OR nombreUsuario LIKE %s'
    cursor.execute(consulta, (busqueda, '%'+ busqueda +'%'))
    usuarios = cursor.fetchall()
    return render_template('busquedaUsuarios.html', usuarios=usuarios, busqueda=busqueda)

#editar usuarios
@app.route('/editar-usuario/<int:id>', methods=['GET', 'POST'])
def editUsuario(id):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE idUsuario = %s', (id,))
    data = cursor.fetchall()
    if req.method == 'POST':
        nombre = req.form['nombre']
        apellido = req.form['apellido']
        nombreUsuario = req.form['nombreUsuario']
        correo = req.form['correo']
        rol = req.form['rol']
    
        sql = 'UPDATE usuarios SET nombre = %s, apellido = %s, nombreUsuario = %s, correo = %s, rol = %s WHERE idUsuario = %s'
        cursor.execute(sql, (nombre, apellido, nombreUsuario, correo, rol, id))
        db.commit()
        return redirect(url_for('listarUsuarios'))
    else:
        return render_template('modalUsuarios.html', data=data[0])

#registrar tareas
@app.route('/registro-tareas', methods=['GET', 'POST'])
def regTareas():
    if req.method == 'POST':
        nombreTarea = req.form.get('nombreTarea')
        fechaInicio = req.form.get('fechaInicio')
        fechaFin = req.form.get('fechaFin')
        estado = req.form.get('estado')
        cursor = db.cursor()
        nombreUsuario = session['nombreUsuario']
        cursor.execute('SELECT * FROM tareas WHERE nombreTarea = %s', (nombreTarea,))
        exist = cursor.fetchone()
        if exist:
            print('Nombre de Tarea existente, asigne uno nuevo')
        else:
            cursor.execute('SELECT idUsuario FROM usuarios WHERE nombreUsuario = %s',(nombreUsuario,))
            idUsuario = cursor.fetchone()
            cursor.execute('INSERT INTO tareas(nombreTarea, fechaInicio, fechaFin, estado, idUsuarioFK) VALUES(%s, %s, %s, %s, %s)',
                        (nombreTarea, fechaInicio, fechaFin, estado, idUsuario[0]))
            db.commit()
            print('tarea registrada')
        cursor = db.cursor(dictionary=True)
        query = ('SELECT nombreUsuario, contraseña, rol FROM usuarios WHERE nombreUsuario = %s')
        cursor.execute(query,(nombreUsuario,))
        userData = cursor.fetchone()
        if userData['rol'] == 'Administrador':
            return redirect(url_for('listarUsuarios'))
        else:
            return redirect(url_for('listarTareas'))
    return render_template('regTareas.html')

#listar tareas de cada usuario
@app.route('/lista-tareas', methods=['GET', 'POST'])
def listarTareas():
    cursor = db.cursor()
    nombreUsuario = session['nombreUsuario']
    cursor.execute('SELECT idUsuario FROM usuarios WHERE nombreUsuario = %s',(nombreUsuario,))
    idUsuario = cursor.fetchone()
    cursor.execute('SELECT * FROM tareas WHERE idUsuarioFK = %s', (idUsuario[0],))
    tareas = cursor.fetchall()
    return render_template('homeUser.html', tareas = tareas)

#listar tareas globales
@app.route('/global-tareas', methods=['GET', 'POST'])
def globalTareas():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM tareas')
    tareas = cursor.fetchall()
    return render_template('globalUser.html', tareas = tareas)

#buscar tareas
@app.route('/buscar-tareas', methods=['POST'])
def buscarTarea():
    busqueda = req.form.get('busqueda')
    cursor = db.cursor(dictionary=True)
    consulta = 'SELECT * FROM tareas WHERE idTarea = %s OR nombreTarea LIKE %s'
    cursor.execute(consulta, (busqueda, '%'+ busqueda +'%'))
    tareas = cursor.fetchall()
    return render_template('busquedaTareas.html', tareas=tareas, busqueda=busqueda)

#eliminar tareas
@app.route('/eliminar-tarea/<int:id>', methods=['GET'])
def delTarea(id):
    cursor = db.cursor()
    cursor.execute('DELETE FROM tareas WHERE idTarea = %s', (id,))
    db.commit()
    return redirect(url_for('globalTareas'))

#editar tareas
@app.route('/editar-tarea/<int:id>', methods=['GET', 'POST'])
def editTarea(id):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM tareas WHERE idTarea = %s', (id,))
    data = cursor.fetchall()
    if req.method == 'POST':
        nombreTarea = req.form['nombreTarea']
        fechaInicio = req.form['fechaInicio']
        fechaFin = req.form['fechaFin']
        estado = req.form['estado']
        nombreUsuario = session['nombreUsuario']
        sql = 'UPDATE tareas SET nombreTarea = %s, fechaInicio = %s, fechaFin = %s, estado = %s WHERE idTarea = %s'
        cursor.execute(sql, (nombreTarea, fechaInicio, fechaFin, estado, id))
        db.commit()
        cursor = db.cursor(dictionary=True)
        query = ('SELECT nombreUsuario, contraseña, rol FROM usuarios WHERE nombreUsuario = %s')
        cursor.execute(query,(nombreUsuario,))
        userData = cursor.fetchone()
        if userData['rol'] == 'Administrador':
            return redirect(url_for('listarUsuarios'))
        else:
            return redirect(url_for('listarTareas'))
    else:
        return render_template('modalTareas.html', data=data[0])

@app.route('/global-stats')
def globalStats():
    cursor = db.cursor()

    cursor.execute('SELECT COUNT(*) FROM usuarios')
    usuarios = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM tareas')
    tareas = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM tareas where estado = "Por Definir"')
    pendientes = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM tareas where estado = "Terminado"')
    terminadas = cursor.fetchone()[0]

    labels = ['Usuarios', 'Tareas', 'Por Definir', 'Terminadas']
    bins = [usuarios, tareas, pendientes, terminadas]
    color = ['slategray', 'olivedrab', 'darkred', 'teal']

    plt.rcParams['font.family'] = 'monospace'
    plt.style.use('dark_background')
    plt.bar(labels, bins, color = color)
    plt.ylabel('Cifras', fontsize = 14)
    plt.xlabel('Datos', fontsize = 14)
    plt.title('Información Global - Gestor de Tareas', fontsize = 16)
    plt.savefig('app/static/img/globalfig.png')
    plt.close()
    return send_file('static/img/globalfig.png', mimetype='image/png')

@app.route('/user-stats')
def userStats():
    cursor = db.cursor()

    nombreUsuario = session['nombreUsuario']
    cursor.execute('SELECT idUsuario FROM usuarios WHERE nombreUsuario = %s', (nombreUsuario,))
    idUsuario = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM tareas WHERE idUsuarioFK = %s', (idUsuario,))
    tareas = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM tareas WHERE estado = "Por Definir" AND idUsuarioFK = %s', (idUsuario,))
    pendientes = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM tareas WHERE estado = "Terminado" AND idUsuarioFK = %s', (idUsuario,))
    terminadas = cursor.fetchone()[0]

    labels = ['Tareas', 'Por Definir', 'Terminadas']
    bins = [tareas, pendientes, terminadas]
    color = ['olivedrab', 'darkred', 'teal']

    plt.rcParams['font.family'] = 'monospace'
    plt.style.use('dark_background')
    plt.bar(labels, bins, color = color)
    plt.ylabel('Cifras', fontsize = 14)
    plt.xlabel('Datos', fontsize = 14)
    plt.title('Información de Usuario - Gestor de Tareas', fontsize = 16)
    plt.savefig('app/static/img/userfig.png')
    plt.close()
    return send_file('static/img/userfig.png', mimetype='image/png')

#cerrar sesión
@app.route("/cerrar", methods=['GET', 'POST'])
def cerrar():
    session.pop('nombreUsuario', None)
    return redirect(url_for('logUsuario'))

#no almacena cache
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = 0
    return response

if __name__ == '__main__':
    app.run(debug=1)
    app.add_url_rule('/', view_func=regTareas)