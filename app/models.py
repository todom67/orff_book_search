from app import db, login_manager, bcrypt

class Book(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(128), nullable=False)
  author = db.Column(db.String(128), nullable=False)
  ISBN = db.Column(db.String(30), nullable=False)
  lpelement_id = db.Column(db.Integer)
  storelink = db.Column(db.String(255))

  def __init__(self, *args, **kwargs):
    super(Book, self).__init__(*args, **kwargs)

  @property
  def lpelements(self):
    binary_as_list = [int(i) for i in bin(self.lpelement_id)[2:]][::-1]
    new_list = [digit * pow(2, index) for index, digit in enumerate(binary_as_list)]
    return list(filter(lambda num: num !=0, new_list))

  def __repr__(self):
    return f"<Book: {self.title} by {self.author}>"

class LPElement(db.Model):
  __tablename__ = 'lpelement'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(128), nullable=False)
  value = db.Column(db.Integer, nullable=False)

  def __init__(self, description, value):
    self.description = description
    self.value = value

  def __repr__(self):
    return f"<LPElement: {self.description} >" 

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(128), unique=True, nullable=False)
  password = db.Column(db.String(128), nullable=False)
  active = db.Column(db.Boolean, default=True)
  admin = db.Column(db.Boolean, default=False)

  def __init__(self, *args, **kwargs):
    super(User, self).__init__(*args, **kwargs)

  def get_id(self):
    return str(self.id)

  def is_authenticated(self):
    return True

  def is_active(self):
    return self.active

  def is_anonymous(self):
    return False

  def is_admin(self):
    return self.admin

  @staticmethod
  def make_password(plaintext):
    return bcrypt.generate_password_hash(plaintext)

  def check_password(self, raw_password):
    return bcrypt.check_password_hash(self.password, raw_password)

  @classmethod
  def create(cls, password, **kwargs):
    return User(
      password=User.make_password(password),
      **kwargs
    )

  @staticmethod
  def authenticate(name, password):
    user = User.query.filter(User.username == name).first()
    if user and user.check_password(password):
      return user
    return False

  def __repr__(self):
    return f"<User: {self.username} >" 

@login_manager.user_loader
def _user_loader(user_id):
  return User.query.get(int(user_id))

