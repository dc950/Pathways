import json
import app
from flask import render_template, session, flash, redirect, url_for, send_from_directory, Flask, request, jsonify, Response
from flask.ext.login import current_user, login_required
from . import main
from .pathway_generator import generate_future_pathway
from .. import db
from ..models import User, UserQualification, Qualification, QualificationType, Career, Subject, Comment
from .forms import EditProfileForm, AddQualificationForm, EditQualificationForm, SearchForm, CommentForm
from ..decorators import admin_required, permission_required
from .search import search_user


@main.route('/')
@main.route('/index')
def index():
    return render_template("index.html",
                           title="Home")


@main.route('/career/<careername>')
def career(careername):
    career_obj = Career.query.filter_by(name=careername).first()
    if career is None:
        flash('Career %s not found.' % careername)
        return redirect(url_for('main.index'))
    return render_template('career.html',
                           career=career_obj,
                           title=careername)


@main.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    user_obj = User.query.filter_by(username=username).first()
    if user_obj is None:
        flash('User %s not found.' % username)
        return redirect(url_for('main.index'))
    form = CommentForm()
    if form.validate_on_submit():
        Comment.add_comment(current_user, user_obj, form.body.data)
    name = user_obj.first_name + " " + user_obj.last_name
    comments = Comment.query.filter_by(profile=user_obj)
    return render_template("user.html",
                           user=user_obj,
                           title=name,
                           comments=comments,
                           form=form)



@main.route('/user/edit-profile', methods=['GET', 'POST'])
@login_required
def edit():
    user_skills = current_user.skills
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.def_avatar = form.default_avatar.data
        db.session.add(current_user)
        flash('Your profile has been updated')
        return redirect(url_for('.user', username=current_user.username))
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    return render_template('edit-profile.html', form=form, skills=user_skills)


@main.route('/user/pathway/edit-qualification/')
@main.route('/user/pathway/edit-qualification/<qualification>', methods=['GET', 'POST'])
@login_required
def edit_qualification(qualification=None):
    """
    These SQL queries should be moved to the model as function eventually
    """
    all_qual_types = QualificationType.query.all()
    user_subjects = UserQualification.query.join(Qualification, UserQualification.qualifications_id==Qualification.id).all()
    user_qual_types = QualificationType.query.join(Qualification, QualificationType.id==Qualification.qualification_type_id).join(UserQualification, UserQualification.qualifications_id==Qualification.id).filter_by(user_id=current_user.id).all()
    user_quals = Qualification.query.join(UserQualification, Qualification.id==UserQualification.qualifications_id).all()
    if qualification is None:
        return render_template("edit-qualification.html",
                           title="Edit Qualifications",
                           show_all=True,
                           subjects=user_subjects,
                           qualifications=user_quals)
    else:
        form = EditQualificationForm()
        form.qualification_type.data = qualification
        return render_template("edit-qualification.html",
                           title="Edit Qualification: " + qualification,
                           show_all=False,
                           form=form)


@main.route('/user/pathway/add-qualification/', methods=['GET', 'POST'])
@login_required
def add_qualification():
    form = AddQualificationForm()

    form.qualification_type.choices = [(q.id, q.name) for q in QualificationType.query.all()]
    form.subjects.choices = [(s.id, s.subject.name) for s in Qualification.query.all()]
    """form.subjects2.query_factory = Qualification.query.all"""

    opt_param = request.args.get("qual_id")

    if opt_param is None:
        print ("Argument not provided")
    else:
        print (opt_param)
        """form.subjects2.query_factory = Qualification.query.filter_by(qualification_type_id = opt_param).all"""

        results = [(s.id, s.subject.name) for s in Qualification.query.filter_by(qualification_type_id=opt_param).all()]
        form.subjects.choices = results
        form.process()

        return jsonify(results)

    if form.validate_on_submit():

        nq = UserQualification()
        nq.user_id = current_user.id
        nq.qualifications_id = form.subjects.data
        nq.grade = 'A*'

        db.session.add(nq)
        db.session.commit()

        return redirect(url_for('main.edit_qualification'))

    return render_template("add-qualification.html",
                            title="Add Qualification",
                            form=form)



@main.route('/connections')
@login_required
def connections():
    users = User.query.all()
    return render_template('connections.html',
                           users=users)


@main.route('/about')
def about():
    return render_template("about.html",
                           title="About Us")


@main.route('/user/pathway', methods=['GET', 'POST'])
@login_required
def pathway():
    user_subjects = UserQualification.query.join(Qualification, UserQualification.qualifications_id==Qualification.id).filter_by().all()
    user_qual_types = QualificationType.query.join(Qualification, QualificationType.id==Qualification.qualification_type_id).join(UserQualification, UserQualification.qualifications_id==Qualification.id).filter_by(user_id=current_user.id).order_by(QualificationType.level).all()
    #user_qual_types = QualificationType.query.join(Qualification, QualificationType.id==Qualification.qualification_type_id).all()

    opt_param = request.args.get("request_json")
    print(opt_param)
    if opt_param is "1":
        #results = dict((t.name, dict(level=t.level, subjects=[
        #        dict(name=s.course_name, grade=s.grade) for s in UserQualification.query.join(Qualification, UserQualification.qualifications_id==Qualification.id).filter_by(qualification_type=t).all()
        #    ])) for t in user_qual_types)
        #print("*** test ***\n")
        results = dict((t.name, dict(level=t.level, subjects=[
                dict(name=s.qualification.subject.name, grade=s.grade) for s in UserQualification.query.join(Qualification, UserQualification.qualifications_id==Qualification.id).filter_by(qualification_type=t).all()
            ])) for t in user_qual_types)

        return jsonify(**results)

    return render_template("pathway.html",
                           title="Your Pathway",
                           subjects=user_subjects)


@main.route('/add_connection/<username>')
@login_required
def add_connection(username):
    user_obj = User.query.filter_by(username=username).first()
    if user_obj is None:
        flash('User does not exist')
        return redirect(url_for('.index'))
    if current_user.made_request(user_obj):
        flash('You have already made a request to this person')
        return redirect(url_for('.user', username=user_obj.username))
    user_obj.send_request(current_user)
    if user_obj in current_user.connections:
        flash('You are now connected with %s.' % (user_obj.first_name + " " + user_obj.last_name))
    else:
        flash('Request sent to %s.' % (user_obj.first_name + " " + user_obj.last_name))
    return redirect(url_for('.user', username=username))


@main.route('/search', methods=['GET', 'POST'])
def search_click():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        term=search_form.term.data
        return redirect(url_for('main.search', term=term))
    flash('Form not validating on submit')
    return redirect(url_for('main.index'))


@main.route('/search/<term>')
def search(term):
    print("in search, term is "+str(term))

    users = search_user(term)
    return render_template("search.html",
                           users=users,
                           term=term)




'''
@main.before_request
def before_request():
    g.search_form = SearchForm()
'''

@main.route('/test')
@admin_required
def test():
    return render_template("test.html",
                           title="Test")

@main.route('/generate-pathway')
def generate_pathway():
    generate_future_pathway()
    return redirect(url_for('main.index'))

@main.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js/pathways.js', path)


@main.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)

'''
/
/user/
/user/edit-profile
/user/pathways
/user/pathways/edit-qualification 
'''
