from ..models import Career, User, Qualification, Skill, UserQualification
from flask.ext.login import current_user
import random

# Check current level
# Get all uni courses with similar fields


def generate_future_pathway():
    uqs = UserQualification.query.filter_by(user_id=current_user.id).all()

    uqs = random.sample(uqs, 3)
    qualifications = []
    for i in uqs:
        qualifications.append(Qualification.query.filter_by(qualification_id=i.qualification_id)).all()

    print(qualifications)
    return qualifications
