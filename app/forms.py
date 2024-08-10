from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    FloatField,
    DateField,
    SelectField,
    DecimalField,
)

from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")


class CampaignForm(FlaskForm):
    name = StringField("Campaign Name", validators=[DataRequired(), Length(max=100)])
    description = TextAreaField("Description", validators=[DataRequired()])
    start_date = DateField("Start Date", validators=[DataRequired()])
    end_date = DateField("End Date", validators=[DataRequired()])
    budget = FloatField("Budget", validators=[DataRequired(), NumberRange(min=0)])
    niche = SelectField(
        "Niche",
        choices=[
            ("technology", "Technology"),
            ("fashion", "Fashion"),
            ("food", "Food"),
            ("travel", "Travel"),
            ("fitness", "Fitness"),
            ("beauty", "Beauty"),
            ("gaming", "Gaming"),
            ("other", "Other"),
        ],
        validators=[DataRequired()],
    )
    visibility = SelectField(
        "Visibility", choices=[("public", "Public"), ("private", "Private")]
    )


class InfluencerSearchForm(FlaskForm):
    niche = SelectField(
        "Niche",
        choices=[
            ("technology", "Technology"),
            ("fashion", "Fashion"),
            ("food", "Food"),
            ("travel", "Travel"),
            ("fitness", "Fitness"),
            ("beauty", "Beauty"),
            ("gaming", "Gaming"),
            ("other", "Other"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Search")


class AdRequestForm(FlaskForm):
    requirements = TextAreaField("Requirements", validators=[DataRequired()])
    payment_amount = DecimalField(
        "Payment Amount", validators=[DataRequired(), NumberRange(min=0)]
    )
    submit = SubmitField("Send Ad Request")


class CampaignSearchForm(FlaskForm):
    niche = SelectField(
        "Niche",
        choices=[
            ("technology", "Technology"),
            ("fashion", "Fashion"),
            ("food", "Food"),
            ("travel", "Travel"),
            ("fitness", "Fitness"),
            ("beauty", "Beauty"),
            ("gaming", "Gaming"),
            ("other", "Other"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Search")


class InfluencerProfileForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    niche = SelectField(
        "Niche",
        choices=[
            ("technology", "Technology"),
            ("fashion", "Fashion"),
            ("food", "Food"),
            ("travel", "Travel"),
            ("fitness", "Fitness"),
            ("beauty", "Beauty"),
            ("gaming", "Gaming"),
            ("other", "Other"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Update Profile")
