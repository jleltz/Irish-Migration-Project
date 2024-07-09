from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired

class PredictionForm(FlaskForm):
    feature1 = FloatField('Current Year Net Migration Percentage of Population (Annual %) - Format: xx.xx', validators=[DataRequired()])
    feature2 = FloatField('Current Year General Surplus/Deficit (Million Euros) - Format: xx.xx', validators=[DataRequired()])
    gdp = FloatField('Current Year GDP per Capita Growth (Annual %) - Format: xx.xx', validators=[DataRequired()])
    inflation_previous_year = FloatField('Last Year Inflation Consumer Prices (Annual %) - Format: xx.xx', validators=[DataRequired()])
    inflation_current_year = FloatField('Current Year Inflation Consumer Prices (Annual %) - Format: xx.xx', validators=[DataRequired()])
    unemployment_previous_year = FloatField('Last Year Unemployment Rate Native Born (Annual %) - Format: xx.xx', validators=[DataRequired()])
    unemployment_current_year = FloatField('Current Year Unemployment Rate Native Born (Annual %) - Format: xx.xx', validators=[DataRequired()])
    submit = SubmitField('Predict')
