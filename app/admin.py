from datetime import datetime
from flask import g, redirect, request, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink

from app import app, db 
from models import Book, LPElement, User

class AdminAuthentication(object):
  def is_accessible(self):
    return g.user.is_authenticated and g.user.is_admin()

class BaseModelView(AdminAuthentication, ModelView):
  pass

class IndexView(AdminIndexView):
  @expose('/')
  def index(self):
    if not (g.user.is_authenticated and g.user.is_admin()):
      return redirect(url_for('login', next=request.path))
    return self.render('admin/index.html', now=datetime.utcnow())

admin = Admin(app, 'Searchinator Admin', index_view=IndexView())
admin.add_view(ModelView(Book, db.session))
admin.add_view(ModelView(LPElement, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_link(MenuLink(name='Back to App', url='/'))