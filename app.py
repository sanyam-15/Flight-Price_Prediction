from flask import Flask,url_for,redirect,render_template,request
import pandas as pd
import joblib
from forms import InputForm
app = Flask(__name__)

app.config['SECRET_KEY']="this_is_a_key"
model=joblib.load("model.joblib")


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", title ="Home")

@app.route('/predict', methods =['GET','POST'])
def predict():
    form = InputForm()
    message = None
    
    if form.validate_on_submit():
        try:
            # Validate source != destination
            if form.source.data == form.destination.data:
                message = "Error: Source and Destination cannot be the same."
            else:
                x_new = pd.DataFrame(dict(
                    airline=[form.airline.data],
                    date_of_journey = [form.date_of_journey.data.strftime("%Y-%m-%d")],
                    source =[form.source.data],
                    destination =[form.destination.data],
                    dep_time = [form.dep_time.data.strftime("%H:%M:%S")],
                    arrival_time =[form.arrival_time.data.strftime("%H:%M:%S")],
                    duration =[form.duration.data],
                    total_stops =[form.total_stops.data],
                    additional_info =[form.additional_info.data]
                ))
                prediction = model.predict(x_new)[0]
                message = f"The predicted price is ₹{prediction:,.0f} for your journey"
        except Exception as e:
            print("Prediction error:", repr(e))
            message = f"Error: {repr(e)}"
    elif request.method == 'POST':
        # Only show validation errors on POST (after form submission)
        # Build a readable error message from form.errors
        error_parts = []
        for field_name, errors in form.errors.items():
            for error in errors:
                error_parts.append(f"{field_name}: {error}")
        message = f"Validation error: {'; '.join(error_parts)}"
    
    return render_template("predict.html", title ="Predict" , form=form , output = message)

if(__name__=="__main__"):
    app.run(debug=True)