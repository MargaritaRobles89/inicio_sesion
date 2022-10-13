from flask_app import app

# Importar los controladores
from flask_app.controllers import users_controller


#Ejecutamos el programa o variable app
if __name__=="__main__":
    app.run(debug=True)