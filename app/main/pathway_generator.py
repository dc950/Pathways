from ..models import Career, User, Qualification, Skill, UserQualification, QualificationType, Field, Subject, CareerSubject
from flask import flash, request, url_for, jsonify
from app import db
import random



def generate_future_pathway(u):

    # Get all fields
    fields = []
    for q in u.qualifications:
        fields.append(q.qualification.subject.field)
    # print("Fields: " + str(fields))

    # count instances of each
    fcount = {}
    for f in fields:
        fcount.update({f: fields.count(f)})

    # sort them 3
    top_fields = fcount.keys()
    top_fields = sorted(top_fields, key=lambda x: fcount[x])
    print(top_fields)
    if len(top_fields) < 2:
        flash("Not enough course data")
        return

    # print("Top fields: "+str(top_fields))

    # Find future qualifications

    # Find next levels
    user_quals = UserQualification.query.filter_by(user_id=u.id).all()
    cur_max_level = max(user_quals, key=lambda x: x.level)

    courses = []

    # For each of the next 3 levels
    for i in range(cur_max_level.level+1, cur_max_level.level+4):
        # If above max value, return
        if i > 8:
            break
        qualification_types = QualificationType.query.filter_by(level=i).all()
        qts = []
        for q in qualification_types:
            chosen_count = 0
            for f in top_fields:
                if chosen_count > 4:
                    break
                possible_courses = Qualification.query.join(
                    Subject, Subject.id == Qualification.subject_id
                ).filter(Qualification.qualification_type_id==q.id).filter_by(field=f).all()
                qt_courses = []
                if len(possible_courses) > 1:
                    qts += random.sample(possible_courses, 2)
                    chosen_count += 2
                elif len(possible_courses) == 1:
                    qts.append(possible_courses[0])
                    chosen_count += 1
        # print("level "+str(i)+": "+str(qts))
        if len(qts) > 3:
            courses += random.sample(qts, 4)
        else:
            courses += qts

    # print("Chosen courses are: " + str(courses))

    # Find future careers

    chosen_count = 0
    careers = []
    for i in top_fields:
        top_careers = Career.query.join(
            CareerSubject, CareerSubject.career_id == Career.id
        ).join(
            Subject, CareerSubject.subject_id == Subject.id
        ).filter_by(field=i).all()
        if len(careers) < 20:
            if len(top_careers) > 10:
                careers += random.sample(top_careers, 10)
                chosen_count += 5
            else:
                careers += top_careers
                chosen_count += 1
        else:
            break

    # Choose best careers based off of the users skills

    # Count number of similar skills for each career
    career_skills = {}
    for c in careers:
        career_skills.update({c: 0})
        for s in c.skills:
            if s in u.skills:
                career_skills.update({c: career_skills[c]+1})

    sorted(careers, key=lambda x: career_skills[x])

    # get top 10
    print(str(careers))
    optimal_careers = careers[:10]
    other_careers = careers[10:]

    if len(optimal_careers) >= 3:
        chosen_careers = random.sample(optimal_careers, 3)
    else:
        chosen_careers = optimal_careers

    spaces_left = 5 - len(chosen_careers)
    print('spaces left: ' + str(spaces_left) + ', len(other_careers): ' + str(len(other_careers)))
    if len(other_careers) >= spaces_left:
        chosen_careers += random.sample(other_careers, spaces_left)
    else:
        chosen_careers += other_careers
        spaces_left = 5 - len(chosen_careers)
        if spaces_left > 0:
            if len([x for x in optimal_careers if x not in chosen_careers]) > spaces_left:
                chosen_careers += random.sample([x for x in optimal_careers if x not in chosen_careers], spaces_left)
            else:
                chosen_careers += optimal_careers

    # print('Top careers: ' + str(top_careers))
    # print("Chosen courses are: " + str(courses))
    # print('Chosen careers are: ' + str(careers))

    u.future_quals = courses
    u.future_careers = chosen_careers


def get_pathway(user):
    user_subjects = UserQualification.query.filter_by(user_id=user.id).join(Qualification, UserQualification.qualifications_id==Qualification.id).all()
    user_qual_types = QualificationType.query.join(Qualification, QualificationType.id==Qualification.qualification_type_id).join(UserQualification, UserQualification.qualifications_id==Qualification.id).filter_by(user_id=user.id).all()

    future_qual_types = [] #.qualification_name
    for x in user.future_quals:
        future_qual_types.append(x.qualification_type)

    for x in user.future_quals:
        uq = UserQualification()
        uq.user_id = user.id
        uq.qualifications_id = x.id
        uq.qualification = x
        user_subjects.append(uq)

    results = dict((("Level " + str(t.level) + " - " + t.name), dict(level=t.level, subjects=[
            dict(name=s.qualification.subject.name, grade=s.grade, field=s.qualification.subject.field.name, future=False) for s in filter((lambda x: x.qualification.qualification_type_id==t.id), user_subjects)
        ])) for t in (user_qual_types + future_qual_types))

    results2 = dict((("Level " + str(9) + " - " + "Careers"), dict(level=9, subjects=[
            dict(name=s.name, grade=None, field=s.qualification.subject.field.name, future=True) for s in user.future_careers
        ])) for t in user_qual_types)

    z = results.copy()
    z.update(results2)
    #z.update(results3)
    return jsonify(**z)
