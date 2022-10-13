from flask import redirect, render_template, request, session
from flask_app import app #importamos al applicación
from flask import flash # se encarga de mostrar mensajes y errores

#importación del modelo 
from flask_app.models.users import User

# importamos Bcrypt para encriptar contraseña
from flask_bcrypt import Bcrypt
bcrypt =  Bcrypt(app)

#rutasindex
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.valida_usuario(request.form):
        return redirect('/')
        
    
    pwd = bcrypt.generate_password_hash(request.form['password'])
    
    formulario = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" :pwd   
    }

    id = User.save(formulario) #recibir el identificador del nuevo usuario
    session['user_id'] = id # guardamos en sesion el identificador del usuario
    
    return redirect('/dashboard')

@app.route('/login',  methods=['POST'])
def login():
    #verificamos que el email exista en la bd
    user  = User.get_by_email(request.form) # Recibimos la instancia del usuario 0 False
    
    if not user:# Si user es falso
        flash('E-mail no encontrado', 'inicio_sesion')
        return redirect ('/')
    #user es una instancia con todos los datos de mi usuario
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Password incorrecto', 'inicio_sesion')
        return redirect ('/')
    
    session['user_id']=user.id
    return redirect('/dashboard')
    
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect ('/')
    
    formulario = {"id": session['user_id']}
    user = User.get_by_id(formulario)
    
    return render_template('dashboard.html', user=user)

    
@app.route('/logout')
def logaut():
    session.clear()
    return redirect ('/')

    