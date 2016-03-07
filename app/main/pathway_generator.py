from ..models import Career, User, Qualification, Skill, UserQualification, QualificationType, Field
from flask.ext.login import current_user
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
        fields.append(q.subject.field)
    print("Fields: " + str(fields))

    # count instances of each
    fcount = {}
    for f in fields:
        fcount.update({f: fields.count(f)})

    # choose top 3
    top_fields = []
    for f in fields:
        if len(top_fields) < 3:
            top_fields.append(f)
        else:
            if fcount[f] > top_fields[-1]:
                top_fields[-1] = f
        top_fields = sorted(top_fields, key = lambda x: fcount[x])

    print("Top fields: "+str(top_fields))
