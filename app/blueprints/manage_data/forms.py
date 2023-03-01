# forms.py

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import InputRequired, Length

from app.extensions import app_db
from app.model import Switch, Location, Fabric

### Switch

class SwitchNewEditFormMixin():

    name = StringField('Name',
                       validators=[InputRequired(), Length(min=2)] )

    fabric = QuerySelectField('Fabric',
                              get_label='name',
                              allow_blank=False,
                              blank_text='Select a fabric',
                              render_kw={'size': 1}
                              )

    location = QuerySelectField('Location',
                              get_label='name',
                              allow_blank=False,
                              blank_text='Select a Location',
                              render_kw={'size': 1}
                              )


class SwitchNewForm(FlaskForm, SwitchNewEditFormMixin):
    submit = SubmitField('Add')

class SwitchEditForm(FlaskForm, SwitchNewEditFormMixin):
    submit = SubmitField('Update')

class SwitchDeleteForm(FlaskForm):
    submit = SubmitField('Confirm delete')

### Fabric

class FabricNewEditFormMixin():

    name = StringField('Name',
                       validators=[InputRequired(), Length(min=2)] )

class FabricNewForm(FlaskForm, FabricNewEditFormMixin):
    submit = SubmitField('Add')

class FabricEditForm(FlaskForm, FabricNewEditFormMixin):
    submit = SubmitField('Update')

class FabricDeleteForm(FlaskForm):
    submit = SubmitField('Confirm delete')

### Location

class LocationNewEditFormMixin():

    name = StringField('Name',
                       validators=[InputRequired(), Length(min=2)] )

class LocationNewForm(FlaskForm, LocationNewEditFormMixin):
    submit = SubmitField('Add')

class LocationEditForm(FlaskForm, LocationNewEditFormMixin):
    submit = SubmitField('Update')

class LocationDeleteForm(FlaskForm):
    submit = SubmitField('Confirm delete')