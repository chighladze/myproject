from flask_wtf import FlaskForm
from wtforms import SelectField


class StudentForm(FlaskForm):
    student = SelectField('student', choices=[], render_kw={'class': 'form-control'})