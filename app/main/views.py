import json
from flask import render_template, flash, redirect, url_for, send_from_directory, request, jsonify, make_response
from flask.ext.login import current_user, login_required
from . import main
from .pathway_generator import generate_future_pathway, get_pathway
from .. import db
from ..models import User, UserQualification, Qualification, QualificationType, Career, Comment, ReportedComment
from .forms import EditProfileForm, AddQualificationForm, EditQualificationForm, SearchForm, CommentForm, SkillsForm
from ..decorators import admin_required
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

    opt_param2 = request.args.get("request_career_page")
    if opt_param2 is not None:
        return url_for('.career', careername=opt_param2)

    opt_param = request.args.get("request_json")
    print(opt_param)
    if opt_param is "1":
        return get_pathway(user_obj)

    form = CommentForm()
    if form.validate_on_submit():
        if contains_bad_word(form.body.data):
            flash('Comment contains an inappropriate word and was not sent')
        else:
            Comment.add_comment(current_user, user_obj, form.body.data)
    name = user_obj.first_name + " " + user_obj.last_name

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


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit():
    user_skills = current_user.skills
    form1 = EditProfileForm()
    form2 = SkillsForm()
    if form1.validate_on_submit():
        print("validated")
        current_user.first_name = form1.first_name.data
        current_user.last_name = form1.last_name.data
        current_user.def_avatar = form1.default_avatar.data
        db.session.add(current_user)
        flash('Your profile has been updated')
        return redirect(url_for('.user', username=current_user.username))
    print(form1.errors)
    form1.first_name.data = current_user.first_name
    form1.last_name.data = current_user.last_name
    form1.default_avatar.data = current_user.def_avatar
    return render_template('edit-profile.html', form1=form1, form2=form2, skills=user_skills)


@main.route('/add-skill/<skill_name>')
@login_required
def add_skill(skill_name):
    current_user.add_skill_name(skill_name)
    response = make_response(json.dumps(True))
    response.content_type = 'application/json'
    return response


@main.route('/delete-skill/<skill_name>')
def delete_skill(skill_name):
    current_user.remove_skill(skill_name)
    response = make_response(json.dumps(True))
    response.content_type = 'application/json'
    return response


@main.route('/edit-qualification/')
@main.route('/edit-qualification/<qualification>', methods=['GET', 'POST'])
@login_required
def edit_qualification(qualification=None):
    """
    These SQL queries should be moved to the model as function eventually
    """
    
    if qualification is None:
        opt_param = request.args.get("delete") 

        if opt_param is not None:
            qual = db.session.query(UserQualification).get((current_user.id, opt_param))
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
        user_qual = db.session.query(UserQualification).get((current_user.id, qualification))
        qual_type = user_qual.qualification.qualification_type_id

        form = EditQualificationForm()
        form.qualification_type.choices = [(q.id, q.name) for q in QualificationType.query.filter_by(id=qual_type).all()]
        form.subjects.choices = sorted([(s.id, s.subject.name) for s in Qualification.query.filter_by(qualification_type_id=qual_type).all()], key=lambda x: x[1])
        form.subjects.default = qualification
        form.grade.default = user_qual.grade

        if form.validate_on_submit():
            user.user_id = current_user.id
            user_qual.qualifications_id = form.subjects.data
            user_qual.grade = form.grade.data

            return redirect(url_for('main.edit_qualification'))

        return render_template("edit-qualification.html",
                           title="Edit Qualification: " + user_qual.qualification.subject.name,
                           show_all=False,
                           form=form)


@main.route('/add-qualification/', methods=['GET', 'POST'])
@login_required
def add_qualification():
    form = AddQualificationForm()

    form.qualification_type.choices = [(q.id, q.name) for q in QualificationType.query.all()]
    form.subjects.choices = sorted([(s.id, s.subject.name) for s in Qualification.query.all()], key=lambda x: x[1])
    """form.subjects2.query_factory = Qualification.query.all"""

    opt_param = request.args.get("qual_id")

    if opt_param is None:
        print("Argument not provided")
    else:
        print(opt_param)
        """form.subjects2.query_factory = Qualification.query.filter_by(qualification_type_id = opt_param).all"""

        results = sorted([(s.id, s.subject.name) for s in Qualification.query.filter_by(qualification_type_id=opt_param).all()], key=lambda x: x[1])
        print(results)
        form.subjects.choices = results
        form.process()

        return jsonify(results)

    if form.validate_on_submit():

        nq = UserQualification()
        nq.user_id = current_user.id
        nq.qualifications_id = form.subjects.data
        nq.grade = form.grade.data

        # Check if this item is already in the database and if it is, overwrite it and return
        oq = UserQualification.query.filter_by(user_id=nq.user_id, qualifications_id=nq.qualifications_id).first()
        if oq is not None:
            oq.grade = nq.grade
        else:
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


@main.route('/pathway', methods=['GET', 'POST'])
@login_required
def pathway():
    opt_param2 = request.args.get("request_career_page")
    if opt_param2 is not None:
        return url_for('.career', careername=opt_param2)

    opt_param = request.args.get("request_json")
    if opt_param is "1":
        return get_pathway(current_user)

    return render_template("pathway.html",
                           title="Your Pathway")


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
