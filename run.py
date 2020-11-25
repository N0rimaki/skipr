import os
from app import create_app
from flask_session import Session

app = create_app()
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

production = os.environ.get("PRODUCTION", False)


if __name__ == '__main__':

    if production:
        app.run(debug=True)
    else:
        app.run(host='127.0.0.1', port=8080, debug=True)