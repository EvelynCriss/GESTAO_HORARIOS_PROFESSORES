from flask import Flask, render_template, session, redirect, url_for
from config import SECRET_KEY, db_config

app = Flask(
    __name__,
    static_folder='views/static',
    template_folder='views/templates'
)
app.secret_key = SECRET_KEY


from controllers import login_controller
from controllers import dashboard_controller
from controllers import professor_controller



login_controller.configura_rotas(app)
dashboard_controller.configura_rotas(app)
professor_controller.configura_rotas(app)



if __name__ == '__main__':
    app.run(debug=True)