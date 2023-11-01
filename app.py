from flask import Flask, render_template, request, jsonify
import pickle


app = Flask(__name__)

# Load the pre-trained model
model = pickle.load(open('heart.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # Get feature values from the form
            age = float(request.form['age'])
            sex = float(request.form['sex'])
            cp = float(request.form['cp'])
            trtbps = float(request.form['trtbps'])
            chol = float(request.form['chol'])
            fbs = float(request.form['fbs'])
            restecg = float(request.form['restecg'])
            thalachh = float(request.form['thalachh'])
            exng = float(request.form['exng'])
            caa = float(request.form['caa'])

            # Input Validation: Check if input values are within acceptable ranges
            # Add more specific validation as needed
            if age < 0 or trtbps < 0 or chol < 0:
                raise ValueError("Invalid input values")

            # Make a prediction using the loaded model
            prediction = model.predict([[age, sex, cp, trtbps, chol, fbs, restecg, thalachh, exng, caa]])

            if prediction[0] == 1:
                result = "High Risk"
            else:
                result = "Low Risk"

            # Route for Displaying the Result
            return render_template('result.html', result=result)

        except Exception as e:
            error_message = "An error occurred during prediction: " + str(e)
            # Error Handling: Display an error message
            return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
