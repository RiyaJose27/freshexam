from flask_app import app
from flask_app.controllers import login
from flask_app.controllers import exam


if __name__=="__main__":
    app.run(debug=True)