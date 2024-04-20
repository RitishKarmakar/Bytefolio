from flask import *
from forms import *

from flask_bcrypt import Bcrypt
 
from email_validator import *
from flask_sqlalchemy import *
app = Flask(__name__)
app.config['SECRET_KEY'] = 'c3cd2ebbf3ec8769038812e04a81e574a0aa9461601dc198'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True , nullable = False)
    email = db.Column(db.String(120), nullable = False)
    image_file = db.Column(db.String(120) , nullable = False ,default = "download.png")
    password = db.Column(db.String(60),nullable = False)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"
@app.route('/Signin', methods = ["GET","POST"])
def SignIn():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'The account is sucessfully Logged in {form.email.data}!','sucess')
        
        print(form.password.data)
        return redirect(url_for('Home'))
    return render_template("signin.html",title ='signin' , form =form)
@app.route('/')
def Home():

    return render_template("home.html")
@app.route('/signup', methods = ["GET","POST"])
def Signup():
    # if request.method=="POST":
    #     Name=request.form.get("user_name")
    #     print(Name)
    #     return render_template("Data_Form.html")
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf -8')
        user = User(username = form.username.data,email = form.email.data,password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'The account is sucessfully created for {form.username.data}!','sucess')
        print(form.username.data)
        print(form.password.data)
        return redirect(url_for('SignIn'))
    return render_template("signup.html",title ='signup' , form =form)

if __name__ == '__main__':
    while True:
        app.run(debug=True)
