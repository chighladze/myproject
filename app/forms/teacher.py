from flask_wtf import FlaskForm
from wtforms import SelectField


class TeacherForm(FlaskForm):
    teacher = SelectField('teacher', choices=[], render_kw={'class': 'form-control'})