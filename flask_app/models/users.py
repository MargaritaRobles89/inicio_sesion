from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash   # se encarga de mostrar mensajes y errores
import re #importando las expresiones regulares
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')# expresion regular de email


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password= data['password']
        self.created_at= data['created_at']
        self.updated_at= data['updated_at']


    @staticmethod
    def valida_usuario(formulario):
        
        es_valido =True
        
        if len(formulario['first_name']) < 3:
            flash('Nombre debe tener al menos tres caracteres', 'registro')
            es_valido = False
            
        if len(formulario['last_name']) < 3:
            flash('Apellido debe tener al menos tres caracteres', 'registro')
            es_valido = False   
            
        if len(formulario['password']) < 6:
            flash('El password debe tener al menos seis caracteres', 'registro')
            es_valido = False     
            
        if formulario['password']!= formulario['confirm_password']:
            flash('Los password no coinciden', 'registro')
            es_valido = False 
            
        if not EMAIL_REGEX.match(formulario['email']):
            flash('E-mail invalido', 'registro')
            es_valido = False
            
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('login_registro').query_db(query, formulario)
        
        if len(results)>=1:
            flash('E-mail registrado previamente', 'registro')
            
        return es_valido
    
    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        result = connectToMySQL('login_registro').query_db(query,formulario)
        return result
    
    @classmethod
    def get_by_email(cls, formulario):
    #formulario = #{ email:mar@gmail.com, password : 1234}
        query = "SELECT * FROM users WHERE email = %(email)s"
        result=connectToMySQL('login_registro').query_db(query, formulario)
        # me regresa una lista [ {id:1, first_name: Maggie..etc}]-->posición  0
        
        if len(result) < 1: #significa que mi lista esta vacia y no existe email
            return False
        else:
            # significa que me regresa una lista con un diccionario/registro
            #correspondiente al usuario de este email
            #result = [ {id:1, first_name: Maggie..etc}]-->posición  0
            
            user = cls(result[0]) 
            #guardo en la variable user el registro encontrado y lo tranfosrmo en una instancia del usuario
            #User( {id:1, first_name: Maggie..etc})
            
            return user # envio la info a users_controllers
    @classmethod
    def get_by_id(cls, formulario):   
        #formulario = {id:1}
        query = "SELECT * from users WHERE id = %(id)s"
        result = connectToMySQL('login_registro').query_db(query, formulario)
        #result = [ {id:1, first_name: Maggie..etc}]-->posición  0
        user = cls(result[0]) #creamos una instancia del usuario
        return user