from ..models import Career, User, Qualification, Skill, UserQualification, QualificationType
from flask.ext.login import current_user
import random

# Check current level
# Get all uni courses with similar fields


def generate_future_pathway():

    # Temporary solution until fields are done.
    # selects a few random uni courses and careers as options
    qualification_type = QualificationType.query.filter_by(name="Bachelor's Degree").first()
    print("QualificationType: "+str(qualification_type.id))
    all_courses = Qualification.query.filter_by(qualification_type=qualification_type).all()
    print("All courses:"+str(all_courses))
    courses = random.sample(all_courses, 5)
    all_careers = Career.query.all()
    branches = []
    for c in courses:
        careers = random.sample(all_careers, 2)
        branch = {'course': c, 'careers': careers}
        branches.append(branch)
    print(str(branches))
