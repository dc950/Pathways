import json
import app
from flask import render_template, session, flash, redirect, url_for, send_from_directory, Flask, request, jsonify, Response, make_response
from flask.ext.login import current_user, login_required
from . import main
from .pathway_generator import generate_future_pathway
from .. import db
from ..models import User, UserQualification, Qualification, QualificationType, Career, Subject, Comment, future_quals, ReportedComment
from .forms import EditProfileForm, AddQualificationForm, EditQualificationForm, SearchForm, CommentForm, SkillsForm
from ..decorators import admin_required, permission_required
from .search import search_user, search_careers
from .profanity_filter import contains_bad_word


@main.route('/')
@main.route('/index')
def index():
    return render_template("index.html",
                           title="Home",
                           noflash=True)


@main.route('/career/<careername>')
def career(careername):
    career_obj = Career.query.filter_by(name=careername).first()
    if career is None:
        flash('Career %s not found.' % careername)
        return redirect(url_for('main.index'))
    return render_template('career.html',
                           career=career_obj,
                           title=careername)


@main.route('/reportcomment/<commentid>')
def reportcomment(commentid):
    comment_obj = Comment.query.filter_by(id=commentid).first()
    reportedalready = ReportedComment.query.filter_by(comment_id=commentid).first()
    if reportedalready:
        flash('You have already reported this comment.')
        return redirect(url_for('main.user',username=current_user.username))
    if comment_obj is None:
        flash('This comment doesnt exist')
        return redirect(url_for('main.user',username=current_user.username))
    ReportedComment.add_comment(comment_obj)
    flash('Thank you for reporting this comment for an Admin to review.')
    return redirect(url_for('main.user',username=current_user.username))

@main.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    user_obj = User.query.filter_by(username=username).first()
    if user_obj is None:
        flash('User %s not found.' % username)
        return redirect(url_for('main.index'))

    if not user_obj.is_active:
        flash('User %s not found.' % username)
        return redirect(url_for('main.index'))

    opt_param = request.args.get("request_json")
    print(opt_param)
    if opt_param is "1":
        results = dict((t.name, dict(level=t.level, subjects=[
                dict(name=s.qualification.subject.name, grade=s.grade) for s in UserQualification.query.filter_by(user_id=user_obj.id).join(Qualification, UserQualification.qualifications_id==Qualification.id).filter_by(qualification_type=t).all()
            ])) for t in QualificationType.query.join(Qualification, QualificationType.id==Qualification.qualification_type_id).join(UserQualification, UserQualification.qualifications_id==Qualification.id).filter_by(user_id=user_obj.id).order_by(QualificationType.level).all())

        return jsonify(**results)

    form = CommentForm()
    if form.validate_on_submit():
        if contains_bad_word(form.body.data):
            flash('Comment contains an inappropriate word and was not sent')
        else:
            Comment.add_comment(current_user, user_obj, form.body.data)
    name = user_obj.first_name + " " + user_obj.last_name

    comments = [] #Comment.query.filter_by(profile=user_obj)

    # comments = Comment.query.filter_by(profile=user_obj)
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.filter_by(profile=user_obj).order_by(Comment.timestamp.desc()).paginate(
        page, per_page=5, error_out=False
    )
    comments = pagination.items
    if user_obj == current_user:
        unseen_comments = current_user.unseen_comments
        for c in unseen_comments:
            c.seen = True
            db.session.add(c)

    return render_template("user.html",
                           user=user_obj,
                           title=name,
                           comments=comments,
                           form=form,
                           pagination=pagination)



@main.route('/user/edit-profile', methods=['GET', 'POST'])
@login_required
def edit():
    user_skills = current_user.skills
    form1 = EditProfileForm()
    form2 = SkillsForm()
    if form1.validate_on_submit():
        print("validated")
        current_user.first_name = form1.first_name.data
        current_user.last_name = form1.last_name.data
        #current_user.email = form1.email.data
        current_user.def_avatar = form1.default_avatar.data
        db.session.add(current_user)
        flash('Your profile has been updated')
        return redirect(url_for('.user', username=current_user.username))
    print(form1.errors)
    form1.first_name.data = current_user.first_name
    form1.last_name.data = current_user.last_name
    #form1.email.data = current_user.email
    form1.default_avatar.data = current_user.def_avatar
    return render_template('edit-profile.html', form1=form1, form2=form2, skills=user_skills)


@main.route('/add-skill/<skill_name>')
@login_required
def add_skill(skill_name):
    # print('In the thing')
    current_user.add_skill_name(skill_name)
    # skills = current_user.skills
    # data = []
    # for s in skills:
    #     data.append(s.name)
    response = make_response(json.dumps(True))
    response.content_type = 'application/json'
    return response


@main.route('/delete-skill/<skill_name>')
def delete_skill(skill_name):
    current_user.remove_skill(skill_name)
    response = make_response(json.dumps(True))
    response.content_type = 'application/json'
    return response


@main.route('/user/pathway/edit-qualification/')
@main.route('/user/pathway/edit-qualification/<qualification>', methods=['GET', 'POST'])
@login_required
def edit_qualification(qualification=None):
    """
    These SQL queries should be moved to the model as function eventually
    """
    
    if qualification is None:
        opt_param = request.args.get("delete") 

        if opt_param is not None:
            qual = db.session.query(UserQualification).get((current_user.id, opt_param))
            #qual = UserQualification.query.filter_by(user_id=current_user.id).filter_by(qualifications_id=opt_param).first()
            db.session.delete(qual)
            db.session.commit()

        user_subjects = UserQualification.query.filter_by(user_id=current_user.id).join(Qualification, UserQualification.qualifications_id==Qualification.id).all()
        user_quals = Qualification.query.join(UserQualification, Qualification.id==UserQualification.qualifications_id).all()

        return render_template("edit-qualification.html",
                           title="Edit Qualifications",
                           show_all=True,
                           subjects=user_subjects,
                           qualifications=user_quals)
        

    else:
        UserQual = db.session.query(UserQualification).get((current_user.id, qualification))
        QualType = UserQual.qualification.qualification_type_id
        form = EditQualificationForm()

        form.qualification_type.choices = [(q.id, q.name) for q in QualificationType.query.filter_by(id=QualType).all()]
        form.subjects.choices = [(s.id, s.subject.name) for s in Qualification.query.filter_by(qualification_type_id=QualType).all()]

        form.subjects.default = qualification

        form.grade.default = UserQual.grade

        #form.process()

        if form.validate_on_submit():
            db.session.delete(UserQual)

            nq = UserQualification()
            nq.user_id = current_user.id
            nq.qualifications_id = form.subjects.data
            nq.grade = form.grade.data

            db.session.add(nq)
            db.session.commit()

            return redirect(url_for('main.edit_qualification'))

        #form.qualification_type.data = qualification
        return render_template("edit-qualification.html",
                           title="Edit Qualification: " + UserQual.qualification.subject.name,
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
        nq.grade = form.grade.data

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
    user_subjects = UserQualification.query.filter_by(user_id=current_user.id).join(Qualification, UserQualification.qualifications_id==Qualification.id).all()
    user_qual_types = QualificationType.query.join(Qualification, QualificationType.id==Qualification.qualification_type_id).join(UserQualification, UserQualification.qualifications_id==Qualification.id).filter_by(user_id=current_user.id).all()
    #user_qual_types = QualificationType.query.join(Qualification, QualificationType.id==Qualification.qualification_type_id).all()

    future_qual_types = [] #.qualification_name
    for x in current_user.future_quals:
        future_qual_types.append(x.qualification_type)

    #user_subjects = current_user.future_quals

    for x in current_user.future_quals:
        uq = UserQualification()
        uq.user_id = current_user.id
        uq.qualifications_id = x.id
        uq.qualification = x
        user_subjects.append(uq)

    # print(current_user.future_quals)

    #user_qual_types.append(future_qual_types)

    #for x in db.session.query(future_quals).filter_by(user_id=current_user.id).all():
    #    print(x.qual_id)
    #      future_qual_types += QualificationType.query.join(Qualification, QualificationType.id==Qualification.qualification_type_id).filter_by(subject_id=x.qual_id).all()
    
    opt_param2 = request.args.get("request_career_page")
    # print(opt_param2)
    if opt_param2 is not None:
        return url_for('.career', careername=opt_param2)

    opt_param = request.args.get("request_json")
    # print(opt_param)
    if opt_param is "1":
        results = dict((("Level " + str(t.level) + " - " + t.name), dict(level=t.level, subjects=[
                dict(name=s.qualification.subject.name, grade=s.grade) for s in filter((lambda x: x.qualification.qualification_type_id==t.id), user_subjects)
            ])) for t in (user_qual_types + future_qual_types))

        results2 = dict((("Level " + str(9) + " - " + "Careers"), dict(level=9, subjects=[
                dict(name=s.name, grade=None) for s in current_user.future_careers
            ])) for t in user_qual_types)

        #results3 = dict((("Level " + str(t.level) + " - " + t.name), dict(level=t.level, test="test")) for t in future_qual_types)

        z = results.copy()
        z.update(results2)
        #z.update(results3)
        return jsonify(**z)


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
    if not user_obj.is_active:
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


@main.route('/remove_connection/<username>')
@login_required
def remove_connection(username):
    user_obj = User.query.filter_by(username=username).first()
    user_obj.remove_connection(current_user)
    if user_obj in current_user.connections:
        flash('User not removed')
    else:
        flash('You have removed your connection with %s.' % (user_obj.first_name + " " + user_obj.last_name))
    return redirect(url_for('.user', username=username))


@main.route('/decline_connection/<username>')
@login_required
def decline_connection(username):
    user_obj = User.query.filter_by(username=username).first()
    user_obj.decline_connection(current_user)
    if user_obj in current_user.connections:
        flash('User not removed')
    else:
        flash('You have declined the connection request with %s.' % (user_obj.first_name + " " + user_obj.last_name))
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
    careers = search_careers(term)
    return render_template("search.html",
                           users=users,
                           careers=careers,
                           term=term)


@main.route('/privacy-policy')
def privacypolicy():
    return render_template("privacy-policy.html")

@main.route('/test')
@admin_required
def test():
    return render_template("test.html",
                           title="Test")


@main.route('/generate-pathway')
def generate_pathway():
    generate_future_pathway(current_user)
    return redirect(url_for('main.pathway'))


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
