import os
from flask_admin import Admin
from models import db, User, Favorites, Species, Planets, People
from flask_admin.contrib.sqla import ModelView

class AdminView(ModelView):
    def __init__(self, model, *args, **kwargs):
        self.column_list = [c.key for c in model.__table__.columns]
        self.form_columns = self.column_list
        super(AdminView, self).__init__(model, *args, **kwargs)

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(AdminView(User, db.session))
    admin.add_view(AdminView(Favorites, db.session))
    admin.add_view(AdminView(Species, db.session))
    admin.add_view(AdminView(Planets, db.session))
    admin.add_view(AdminView(People, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))