from ..models import Career, User, Qualification, Skill, UserQualification, QualificationType, Field, Subject
from flask.ext.login import current_user
from app import db
import random


# Check current level
# Get all uni courses with similar fields


def generate_future_pathway(u):
    # Temporary solution until fields are done.
    # selects a few random uni courses and careers as options
    # qualification_type = QualificationType.query.filter_by(name="Bachelor's Degree").first()
    # print("QualificationType: "+str(qualification_type.id))
    # all_courses = Qualification.query.filter_by(qualification_type=qualification_type).all()
    # print("All courses:"+str(all_courses))
    # courses = random.sample(all_courses, 5)
    # all_careers = Career.query.all()
    # branches = []
    # for c in courses:
    #     careers = random.sample(all_careers, 2)
    #     branch = {'course': c, 'careers': careers}
    #     branches.append(branch)
    # print(str(branches))

    # Actual solution
    # Find most common field based on qualifications
    qualification_type = QualificationType.query.filter_by(name="Bachelor's Degree").first()

    # Get all fields
    fields = []
    for q in u.qualifications:
        fields.append(q.qualification.subject.field)
    print("Fields: " + str(fields))

    # count instances of each
    fcount = {}
    for f in fields:
        fcount.update({f: fields.count(f)})

    # sort them 3
    top_fields = fcount.keys()
    top_fields = sorted(top_fields, key=lambda x: fcount[x])

    print("Top fields: "+str(top_fields))

    # Find some courses using those fields (eventually check requirements as well)

    # Takes two from most common and one from each other
    top_courses = Qualification.query.join(Subject).filter_by(field=top_fields[0]).filter_by(name="Bachelor's Degree").all()
    # Randomly pick two
    courses = random.sample(top_courses, 2)

    # Get one from each of the others:
    course = Qualification.query.join(Subject).filter_by(field=top_fields[1]).filter_by(name="Bachelor's Degree").all()
    courses.append(random.sample(course, 1)[0])
    course = Qualification.query.join(Subject).filter_by(field=top_fields[2]).filter_by(name="Bachelor's Degree").all()
    courses.append(random.sample(course, 1)[0])
    # TODO: Check for entry requirements

    print("Chosen courses are: " + str(courses))

    # Find career for field of each course
    all_careers = Career.query.all()
    # for c in all_careers:
    #     print(str(c.field))

    top_careers = []
    chosen_count = 0
    careers = []
    for i in top_fields:
        top_careers = list(filter(lambda c: i in c.fields, all_careers)) # TODO: change to big join thing to speed up
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

    print('Top careers: ' + str(top_careers))
    print("Chosen courses are: " + str(courses))
    print('Chosen careers are: ' + str(careers))

    u.future_quals = courses
    u.future_careers = careers

