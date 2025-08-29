from .packages import *

from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
    
admin = Admin(app=app)


class UserModelView(ModelView):
    
    def is_accessible(self):
        if session.get("administrator"):  
            #flash("لطفا در کار با داده ها دقت کنید")
            return redirect(url_for("signin"))

    can_delete = False  # disable model deletion
    page_size = 50  # the number of entries to display on the list view
    can_export = True
    column_exclude_list = ['password']
    form_excluded_columns = ['registration']

class TransactionsModelView(ModelView):
    
    def is_accessible(self):
        if session.get("administrator"):  
            #flash("لطفا در کار با داده ها دقت کنید")
            return redirect(url_for("signin"))

    can_delete = False  # disable model deletion
    page_size = 100  # the number of entries to display on the list view
    can_export = True
    column_exclude_list = ['description','content']
    form_excluded_columns = ['registration']


admin.add_view(UserModelView(User,db.session))
admin.add_view(TransactionsModelView(Transactions,db.session))