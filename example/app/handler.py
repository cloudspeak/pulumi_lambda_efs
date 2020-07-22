from apig_wsgi import make_lambda_handler
from sample_django.wsgi import application

"""
This is the main Lambda handler.  It passes calls to the Django application.
"""

lambda_handler = make_lambda_handler(application)
