from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mssql+pyodbc://@LAPTOP-1IIN9JKI\\SQLEXPRESS/spacesphere?"
    "driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

class User(db.Model):
    __tablename__ = "spaceusers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50),primary_key = True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(255),nullable = False)
    address = db.Column(db.String(50))
    number = db.Column(db.String(50))

with app.app_context():
    db.create_all()

@app.route("/")

def home():

    return render_template("index.html")


@app.route("/",methods=["GET","POST"])

def submit():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password)
        address = request.form['address']
        number = request.form['number']

        new_user = User(
             username = username,
             email = email,
             password = hashed_password,
             address = address,
             number = number
             
        )

        db.session.add(new_user)
        db.session.commit()

        print(username, email, password, address, number)
        

    return render_template("index.html")




if __name__ == "__main__":

        app.run(debug=True)
