from flask import Flask, flash, render_template, request, redirect, url_for
import os, re, MySQLdb
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


app = Flask(__name__)
app.secret_key = 'sdkfajl'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://rationshop:password@localhost/rationshop'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    password = db.Column(db.String(128))
    number = db.Column(db.String(16))
    address = db.Column(db.String(128))
    category = db.Column(db.String(10))
    member_count = db.Column(db.Integer)

    def __repr__(self):
        return self.name

    #allotments = relationship( 'Allotment', backref=db.backref('users'))

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __repr__(self):
        return self.name

class Allotment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    user = relationship('User', backref='allotments')
    item_id = db.Column(db.Integer, ForeignKey('item.id'))
    item = relationship('Item', backref='allotments')
    amount = db.Column(db.Float)


class AllotmentView(ModelView):
    form_ajax_refs = {
            'user': {
                'fields': ['name'],
                'page_size': 10
                },
            'item': {
                'fields': ['name'],
                'page_size': 10
                }
            }



admin = Admin(app, name='Rationshop', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Item, db.session))
admin.add_view(AllotmentView(Allotment, db.session))

@app.route('/auth', methods=['POST'])
def authenticate():
    user = db.session.query(User).filter(User.name == request.form['name']).\
            filter(User.password == request.form['password']).first()
    if (user):
        return user.name + ',' + user.number + ',' + user.address + ',' + user.category
    return '0'

if __name__ == '__main__':
    app.debug = True
    manager.run()

