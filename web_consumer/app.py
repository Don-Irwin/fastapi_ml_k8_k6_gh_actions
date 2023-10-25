#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, jsonify,escape,make_response
from flask import Blueprint
# from flask.ext.sqlalchemy import SQLAlchemy
import json
import logging
import random
from logging import Formatter, FileHandler
from forms import *
import os, time
from os import stat_result
from flask import Flask, render_template, url_for, request, redirect, flash,get_flashed_messages ,Markup
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import Integer
from sqlalchemy.schema import MetaData, Table, Column, ForeignKey
from datetime import datetime
import uuid
import string
from os import environ
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from libraries.import_export_data_objects import import_export_data as Import_Export_Data
from libraries.altair_renderings import AltairRenderings
from libraries.utility import Utility
import altair as alt
from datetime import timedelta
import glob
from flask_recaptcha import ReCaptcha
import warnings
warnings.filterwarnings("ignore")

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)

app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///get_my_post_card.db'

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "mids.2022.fall.w210.th.4.tm.4@gmail.com",
    "MAIL_PASSWORD": "gtzanwbkhmkhoqyq"
}

app.config.update(mail_settings)
mail = Mail(app)


# Dev Recaptcha 127
app.config['RECAPTCHA_SITE_KEY'] = '6LdHDbYdAAAAAGD_3EXjO6pgrwT6-99dGXTKDnsW'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdHDbYdAAAAAGD_3EXjO6pgrwT6-99dGXTKDnsW'
app.config['RECAPTCHA_SECRET_KEY'] = '6LdHDbYdAAAAAHQvFxj10731OQ3eF1UF5b_skayo'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdHDbYdAAAAAHQvFxj10731OQ3eF1UF5b_skayo'
app.config['RECAPTCHA_USE_SSL']= False



recaptcha = ReCaptcha(app) 


db = SQLAlchemy(app)

import jinja2                                                                                                                                                                                                  
                                                                                                                                                                                     
def include_file(ctx, name):                                                                                                                                                                                   
    env = ctx.environment                                                                                                                                                                                      
    return jinja2.Markup(env.loader.get_source(env, name)[0])
    
def is_local_host():
    url = str(request.url_root)
    if url.__contains__("127.0.0.1"):
        return True
    else:
        return False

def get_carousel_width():
    if is_local_host():
        slide_show_width = 725
    else:
        slide_show_width = 725
    return slide_show_width

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/clearthisuser', methods=['POST', 'GET'])
def clear_this_user():
    res = make_response("clear cookies")
    expire_date = datetime.now()
    expire_date = expire_date + timedelta(minutes=-10)
    res.delete_cookie('sessionID')
    return res

def check_if_new_user():
    for key in request.cookies.keys():
        print("key=",key)
        if key=='sessionID':
            print("FOUND THE DEALIO")
            return False

    return True


@app.route('/', methods=['POST', 'GET'])
def home():

    is_new_user = check_if_new_user()

    print("*"*80)
    print("is_new_user=",is_new_user)
    print("*"*80)
    

    res = make_response(render_template('pages/placeholder.home.html',
        is_new_user=is_new_user))
    res.set_cookie('sessionID', 'fido',max_age=60*10)
    return res




# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')




@app.route('/send_email', methods=['POST', 'GET'])
def send_email():

    form = email_form()
    success = False
    slide_show_width = get_carousel_width()    
    if request.method == 'POST':
        form = email_form(request.form)
        if not form.validate():
            print("bozo")
            return jsonify({'htmlresponse': render_template('modal/email_modal.html',form=form,already_registered_email=None,is_verified=None,slide_show_width=slide_show_width,success=success)})
        else:
            print("valid")
            first_name = request.form["first_name"] 
            email_address = request.form["email_address"]
            message_text = request.form["message_text"]
            line_break = '\n'  # used to replace line breaks with html breaks

            email_body = "Email from w210 Project "+ datetime.now().strftime("%d-%b-%Y-%H:%M:%S") + "\n" \
                         "Sender's Name: " + first_name + "\n" \
                         "Sender's Email: " + email_address + "\n\n" \
                         "Sender's Message: \n\n" + message_text + "\n\n" \

            with app.app_context():
                msg = Message(subject="Email From MIDS W210 Project Fall 2022 "+ datetime.now().strftime("%d-%b-%Y-%H:%M:%S"),
                              sender=app.config.get("MAIL_USERNAME"),
                              recipients="don.irwin@berkeley.edu".split(","),  # replace with your email for testing
                              body=email_body)
                mail.send(msg)
                print("success=",True)
                success=True

            return jsonify({'htmlresponse': render_template('modal/email_modal.html',form=form,already_registered_email=None,is_verified=None,slide_show_width=slide_show_width,success=success)})
    else:
        return jsonify({'htmlresponse': render_template('modal/email_modal.html',form=form,already_registered_email=None,is_verified=None,slide_show_width=slide_show_width,success=success)})


#----------------------------------------------------------------------------#
# Get Individual PY files
#----------------------------------------------------------------------------#


# from section_1 import section_1
# app.register_blueprint(section_1)
# from section_2 import section_2
# app.register_blueprint(section_2)
# from section_3 import section_3
# app.register_blueprint(section_3)
# from section_4 import section_4
# app.register_blueprint(section_4)

# from section_5 import section_5
# app.register_blueprint(section_5)
# from section_6 import section_6
# app.register_blueprint(section_6)
# from section_7 import section_7
# app.register_blueprint(section_7)

# from fastapi_consumer import fastapi_consumer
# app.register_blueprint(fastapi_consumer)
from consume_fastapi import consume_fastapi
app.register_blueprint(consume_fastapi)




#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0', port=5023)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
'''

    # with app.app_context():
    #     msg = Message(subject="Hello",
    #                   sender=app.config.get("MAIL_USERNAME"),
    #                   recipients="don.irwin@berkeley.edu".split(), # replace with your email for testing
    #                   body="This is a test email I sent with Gmail and Python!")
    #     mail.send(msg)    
