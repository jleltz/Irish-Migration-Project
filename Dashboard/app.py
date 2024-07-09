from flask import Flask, render_template, request, redirect, url_for
import joblib
from forms import PredictionForm
import statsmodels.api as sm
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Load the model
model_fit = joblib.load('C:\\Users\\joosl\\Downloads\\Courses\\Dissertation\\model_fit.pkl')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PredictionForm()
    prediction = None
    lower_bound = None
    upper_bound = None

    if form.validate_on_submit():
        # Get the data from the form
        # feature1 = form.feature1.data
        # feature2 = form.feature2.data
        # feature3 = form.feature3.data
        
        gdp = form.gdp.data
        inflation_previous_year = form.inflation_previous_year.data
        inflation_current_year = form.inflation_current_year.data
        unemployment_previous_year = form.unemployment_previous_year.data
        unemployment_current_year = form.unemployment_current_year.data
        feature1 = form.feature1.data
        feature2 = form.feature2.data
        crisis_indicator = 0

        # Check GDP (if negative, it is a crisis indicator)
        if gdp <= 0:
            crisis_indicator += 1
        
        # Check Inflation (if inflation is decreasing, it is a crisis indicator)
        if inflation_current_year < inflation_previous_year:
            crisis_indicator += 1
        
        # Check Unemployment (if unemployment is increasing, it is a crisis indicator)
        if unemployment_current_year > unemployment_previous_year:
            crisis_indicator += 1
            
        # Create a DataFrame for the model with an index
        input_data = pd.DataFrame({
            'const': [1],  # Add the intercept term manually
            'T-1 Migration Percentage of Population': [feature1], 
            'T-1 General Surplus/Deficit (Million Euros)': [feature2],
            'T-1 Crisis Indicator': [crisis_indicator]
        }, index=[0])

        # Make a prediction
        prediction = model_fit.predict(input_data)[0]
        predictions = model_fit.get_prediction(input_data)
        confidence_intervals = predictions.conf_int(alpha=0.05)
        lower_bounds = confidence_intervals[:, 0]
        upper_bounds = confidence_intervals[:, 1]



        
        # Round the prediction to 2 decimal places and add a percentage sign
        prediction = f'{prediction:.2f}%'

        # Round the confidence intervals to 2 decimal places and add a percentage sign
        lower_bound = f'{lower_bounds[0]:.2f}%'
        upper_bound = f'{upper_bounds[0]:.2f}%'


        return render_template('index.html', form=form, prediction=prediction, lower_bound=lower_bound, upper_bound=upper_bound)
    
    return render_template('index.html', form=form, prediction=prediction, lower_bound=lower_bound, upper_bound=upper_bound)

if __name__ == '__main__':
    app.run(debug=True)