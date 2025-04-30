from flask import Flask, render_template, redirect, request, url_for, session
from config import Config
from extencions import db, init_extencions, login_manager
from models import User
from flask_sqlalchemy import SQLAlchemy 
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from werkzeug.security import check_password_hash, generate_password_hash
import os 

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

with app.app_context():
    db.create_all()

app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/iniciar_sesion')
def login():
    return render_template('login.html')

@app.route('/principal')
def princi():
    nombre = session.get('nmbre')
    return render_template('principal.html', nombre=nombre)

@app.route('/lista_usuarios')
def lista_usuarios():
    usuarios=User.query.all()
    return render_template("usuarios.html", usuarios=usuarios)

@app.route('/registrar', methods=['POST'])
def registrar():
    nombre=request.form['nombre']
    correo=request.form['correo']
    password_plana = request.form['password']
    password_hasheada = generate_password_hash(password_plana)

    usuario_existente = User.query.filter_by(correo=correo).first()
    if usuario_existente:
        flash('este correo ya ha sido registrado','error')
        return redirect('/')

    nuevo_usuario = User(nombre=nombre, correo=correo, password=password_hasheada)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return redirect('/iniciar_sesion')

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    usuario = User.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect('/')

@app.route('/cambiar/<int:id>', methods=['GET','POST'])
def cambiar_usuario(id):
    usuario = User.query.get_or_404(id)

    if request.method == 'POST':

        usuario.nombre = request.form['nombre']
        usuario.correo = request.form['correo']
        usuario.password = request.form['password']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('cambiar_usuario.html', usuario=usuario)



@app.route('/login', methods=['GET','POST'])
def iniciar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']

        usuarios = User.query.all()
        for u in usuarios:
            print(f"En base: '{u.nombre}'")

        print(f"nombre recibido: '{nombre}'")

        user=User.query.filter_by(nombre=nombre).first()

        print(f"usuario encontrado: {user}")

        if user and check_password_hash(user.password, password):
            login_user(user)
            session['nmbre'] = user.nombre
            return redirect('/principal')
    
    
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)

# host="0.0.0.0", port=5000,
# ctrl+} == #
