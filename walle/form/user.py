# -*- coding: utf-8 -*-
"""
    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-03-19 15:50:07
    :author: wushuiyong@walle-web.io
"""
try:
    from flask_wtf import FlaskForm  # Try Flask-WTF v0.13+
except ImportError:
    from flask_wtf import Form as FlaskForm  # Fallback to Flask-WTF v0.12 or older
import re
from flask_wtf import Form
from walle.model.user import UserModel
from werkzeug.security import generate_password_hash
from wtforms import PasswordField, StringField
from wtforms import validators, ValidationError
from wtforms.validators import Regexp


class UserForm(FlaskForm):
    email = StringField('email', [validators.email()])
    password = PasswordField('Password', [validators.Length(min=6, max=35),
                                          validators.Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{6,}",
                                                            message='密码至少6个字符，至少1个大写字母，1个小写字母，1个数字')])

    username = StringField('Username', [validators.Length(min=1, max=50)])
    role = StringField('role', [])

    def validate_email(self, field):
        if UserModel.query.filter_by(email=field.data).first():
            raise ValidationError('Email already register')

    def form2dict(self):
        return {
            'username': self.username.data,
            'password': generate_password_hash(self.password.data),
            'email': self.email.data,
            'role': self.role.data if self.role.data else '',
        }


class RegistrationForm(UserForm):
    pass


class UserUpdateForm(Form):
    password = PasswordField('Password', [])
    username = StringField('username', [])

    def validate_password(self, field):
        if field.data and not re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{6,}", field.data):
            raise ValidationError('密码至少6个字符，至少1个大写字母，1个小写字母，1个数字')


class LoginForm(Form):
    email = StringField('email', [validators.Length(min=6, max=35),
                                  Regexp(r'^(.+)@(.+)\.(.+)', message='邮箱格式不正确')])
    password = PasswordField('Password', [validators.Length(min=6, max=35)])
