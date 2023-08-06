# -*- coding: utf-8 -*-
from .test import *

INSTALLED_APPS = INSTALLED_APPS + ('django_jenkins',)

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
    'django_jenkins.tasks.run_flake8',
    'django_jenkins.tasks.with_coverage',
    #'django_jenkins.tasks.django_tests',
)
