from flask import Blueprint, abort, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..extensions import db
from ..models.post import Post
from ..models.user import User
from ..forms.student import StudentForm
from ..forms.teacher import TeacherForm

post = Blueprint('post', __name__)


@post.route('/', methods=['GET', 'POST'])
def all():
    form = TeacherForm()
    form.teacher.choices = ['Все посты']+[t.name for t in User.query.filter_by(status='teacher')]

    if request.method == 'POST' and request.form['teacher'] != 'Все посты':
        teacher = request.form['teacher']
        teacher_id = User.query.filter_by(name=teacher).first().id
        posts = Post.query.filter_by(teacher=teacher_id).order_by(Post.date.desc()).all()
    else:
        posts = Post.query.order_by(Post.date.desc()).all()
    return render_template('post/all.html',
                           form=form,
                           posts=posts,
                           user=User
                           )


@post.route('/post/create', methods=['GET', 'POST'])
@login_required
def create():
    form = StudentForm()
    form.student.choices = [s.name for s in User.query.filter_by(status='user')]
    if request.method == 'POST':
        subject = request.form.get('subject')
        student = request.form.get('student')
        student_id = User.query.filter_by(name=student).first().id

        post = Post(teacher=current_user.id, subject=subject, student=student_id)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(str(e))
            return render_template('post/create.html')
    else:
        return render_template('post/create.html', form=form)


@post.route('/post/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    post = Post.query.get_or_404(id)
    if post.author.id == current_user.id:
        form = StudentForm()
        form.student.data = User.query.filter_by(id=post.student).first().name
        form.student.choices = [s.name for s in User.query.filter_by(status='user')]
        if request.method == 'POST':
            post.subject = request.form.get('subject')
            student = request.form.get('student')

            post.student = User.query.filter_by(name=student).first().id

            try:
                db.session.commit()
                return redirect('/')
            except Exception as e:
                print(str(e))
                return render_template('post/all.html')
        else:
            return render_template('post/update.html', post=post)
    else:
        # abort(403)
        return render_template('main/_403.html')


@post.route('/post/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    if post.author.id == current_user.id:
        try:
            db.session.delete(post)
            db.session.commit()
            return redirect(url_for('post.all'))
        except Exception as e:
            print(str(e))
            return str(e)
    else:
        # abort(403)
        return render_template('main/_403.html')
