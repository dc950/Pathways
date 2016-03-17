#!/usr/bin/env python

import os
from app import create_app, db
from app.models import User, Skill, Career, Qualification, QualificationType, Role, Permission, Subject, Field
from app.admin.qualifications import DefineQualificationTypes, DefineFields, setup, QualificationsClear

from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

print("Starting in " + (os.getenv('FLASK_CONFIG') or 'default') + " mode")
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Skill=Skill, Career=Career, Qualification=Qualification, DefineFields=DefineFields,
            QualificationType=QualificationType, Role=Role, Permission=Permission, #DefineSubjects=DefineSubjects, 
            DefineQualificationTypes=DefineQualificationTypes, Subject=Subject, Field=Field, setup=setup,
            QualificationsClear=QualificationsClear)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
#manager.add_command("setup", Setup)


@manager.command
def test():
    # Run unit tests
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
