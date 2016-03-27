from ..models import Career, User, Qualification, Skill, UserQualification, QualificationType, Field, Subject, CareerSubject
from flask import flash
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
        if chosen_count == 0:
            if len(top_careers) > 1:
                careers = random.sample(top_careers, 2)
                chosen_count += 1
            elif len(top_careers) == 1:
                careers = random.sample(top_careers, 1)
                chosen_count += 1
        elif chosen_count > 0 and chosen_count < 3:
            if len(top_careers) > 0:
                careers.append(random.sample(top_careers, 1)[0])
                chosen_count += 1
        else:
            break

    # print('Top careers: ' + str(top_careers))
    # print("Chosen courses are: " + str(courses))
    # print('Chosen careers are: ' + str(careers))

    u.future_quals = courses
    u.future_careers = careers
