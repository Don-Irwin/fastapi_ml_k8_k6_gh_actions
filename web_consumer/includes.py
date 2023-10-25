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