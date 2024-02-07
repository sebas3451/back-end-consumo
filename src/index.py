from app import app
from utils.db import db

db.init_app(app)
with app.app_context():
    db.create_all()
    

if __name__ == "__main__":
    app.run(host= "0.0.0.0", debug=True, port = 5000, threaded=True)