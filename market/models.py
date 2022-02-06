from flask_login.login_manager import LoginManager
from market import db, login_man
from market import bcrypts
from flask_login import UserMixin

@login_man.user_loader
def load_user(id_user):
    return User.query.get(int(id_user))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f"{str(self.budget)[:-3]},{str(self.budget)[-3:]}$"
        else:
            return f"{self.budget}$"

    @property
    def password(self):
        return self.password    

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypts.generate_password_hash(plain_text_password).decode("utf-8")

    def password_check(self,thepass):
        return bcrypts.check_password_hash(self.password_hash, thepass)


