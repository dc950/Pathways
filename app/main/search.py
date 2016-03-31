from ..models import User, Career, Subject, CareerSubject, Field, CareerSkill, Skill
from sqlalchemy import and_


def remove_doubles(l):
    new_l = []
    for i in l:
        if i not in new_l:
            new_l.append(i)
    return new_l


def search_user(term):

    users = []
    print("Searching for " + term)
    # No space - search first and last names (and usernames)
    if ' ' not in term:
        print("1 word")
        # Try to get exact matches first:
        users += User.query.filter_by(first_name=term).all()
        users += User.query.filter_by(last_name=term).all()
        users += User.query.filter_by(username=term).all()

        # Try to get close matches next
        users += User.query.filter(User.first_name.like('%'+term+'%')).all()
        users += User.query.filter(User.last_name.like('%'+term+'%')).all()
        users += User.query.filter(User.username.like('%'+term+'%')).all()
    else:
        # 1 or more spaces - find all combinations (some names might have a space in them...)
        words = term.split(' ')
        names = []
        for i in range(1, len(words)):
            first_name = ''
            last_name = ''
            # Get all previous names
            for fn in words[:i]:
                first_name += fn + ' '
            first_name = first_name[:-1]
            # get all future names
            for ln in words[i:]:
                last_name += ln + ' '
            # Get rid of last space
            last_name = last_name[:-1]
            print("Searching fn="+first_name+", ln="+last_name)
            names.append((first_name, last_name))
        # Loop through the names to get exact matches first so they are at the top of the list
        for first_name, last_name in names:
            users += (User.query.filter_by(first_name=first_name, last_name=last_name, is_active=True).all())
        # Loop through again looking for close matches
        for first_name, last_name in names:
            users += User.query.filter(and_(User.first_name.like('%'+first_name+'%'), User.last_name.like('%'+last_name+'%'))).all()
        # TODO: More stuff to expand further
    users = remove_doubles(users)
    for u in users:
        if not u.is_active:
            users.remove(u)
    return users


def search_careers(term):

    careers = []
    careers += Career.query.filter_by(name=term).all()
    careers += Career.query.filter(Career.name.like('%'+term+'%')).all()

    # Add from subject
    careers += Career.query.join(
        CareerSubject, Career.id == CareerSubject.career_id
    ).join(
        Subject, CareerSubject.subject_id == Subject.id
    ).filter(Subject.name.like('%'+term+'%')).all()

    # Add from field
    careers += Career.query.join(
        CareerSubject, Career.id == CareerSubject.career_id
    ).join(
        Subject, CareerSubject.subject_id == Subject.id
    ).join(
        Field, Subject.field_id == Field.id
    ).filter(Field.name.like('%'+term+'%')).all()

    # Add from skill
    careers += Career.query.join(
        CareerSkill, Career.id == CareerSkill.career_id
    ).join(
        Skill, CareerSkill.skills_id == Skill.id
    ).filter(Skill.name.like('%'+term+'%')).all()

    careers = remove_doubles(careers)

    return careers
