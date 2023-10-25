from flask_wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, SelectField,HiddenField,DecimalField
# from wtforms.fields.html5 import DecimalRangeField
from wtforms.validators import DataRequired, EqualTo, Length,Email,Optional
from libraries.import_export_data_objects import import_export_data as Import_Export_Data
from libraries.data_objects import data_objects as do

# Set your classes here.

class home_predict_model_inputs(Form):
    mdo = do()
    medinc_list     = SelectField('medinc_list',choices=mdo.hh_income_tuple())
    houseage_list   = SelectField('houseage_list',choices=mdo.h_age_tuple())
    averooms_list   = SelectField('averooms_list',choices=mdo.avg_beds_tuple())
    avebedrms_list  = SelectField('avebedrms_list',choices=mdo.avg_beds_tuple())
    population_list = SelectField('population_list',choices=mdo.bg_pop_tuple())
    aveoccup_list   = SelectField('aveoccup_list',choices=mdo.avg_occupacy())
    cities_list     = SelectField('cities_list',choices=mdo.ca_city_lat_long_tuple())

    medinc_text     = DecimalField('medinc_text',places=6,validators=[DataRequired("*")])
    houseage_text   = DecimalField('houseage_text',places=6,validators=[DataRequired("*")])
    averooms_text   = DecimalField('averooms_text',places=6,validators=[DataRequired("*")])
    avebedrms_text  = DecimalField('avebedrms_text',places=6,validators=[DataRequired("*")])
    population_text = DecimalField('population_text',places=6,validators=[DataRequired("*")])
    aveoccup_text   = DecimalField('aveoccup_text',places=6,validators=[DataRequired("*")])
    lat_text        = DecimalField('lat_text',places=6,validators=[DataRequired("*")])
    long_text       = DecimalField('long_text',places=6,validators=[DataRequired("*")])


class email_form(Form):

    first_name = TextField(
        'first_name', validators=[DataRequired(message="First name required"), Length(min=3, max=25)]
    )
    email_address = TextField(
        'email_address', validators=[Email(message="Please enter a valid email address"), Length(min=6, max=60),DataRequired()]
        # email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
        #email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    )
    message_text = TextField(
        'message_text', validators=[DataRequired(message="Please enter a text message."), Length(min=4, max=600)]
    )



class RegisterForm(Form):
    name = TextField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )

class sign_up_form(Form):

    first_name = TextField(
        'first_name', validators=[DataRequired(message="First name requrired"), Length(min=6, max=25)]
    )
    last_name = TextField(
        'last_name', validators=[DataRequired(message="Last name required"), Length(min=6, max=25)]
    )
    email_address = TextField(
        'email_address', validators=[Email(message="Please enter a valid email address"), Length(min=6, max=60)]
    )
    address_1 = TextField(
        'address_1', validators=[DataRequired(message="Please enter an address"), Length(min=6, max=60)]
    )
    address_2 = TextField(
        'address_2', validators=[Optional(), Length(min=6, max=60)]
    )
    address_3 = TextField(
        'address_3', validators=[Optional(), Length(min=6, max=60)]
    )
    city = TextField(
        'city', validators=[DataRequired(message="Please enter a valid City."), Length(min=6, max=60)]
    )
    state = TextField(
        'state', validators=[DataRequired(message="Please enter a valid State."), Length(min=6, max=60)]
    )
    country = TextField(
        'country', validators=[DataRequired(message="Please enter a valid country"), Length(min=6, max=60)]
    )
    postal_code = TextField(
        'postal_code', validators=[DataRequired(message="Please enter a valid postal code"), Length(min=6, max=60)]
    )
    recaptcha = RecaptchaField()


class LoginForm(Form):
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
