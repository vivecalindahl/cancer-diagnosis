'''
TODO/Improvements
- Error handling: currently handled by assertion/ValueError.  This is not great as the client gets no informative error message. Better would be to extend the response format to give information about the error:
    {
    "status": "error",
    "error_code": "400",
    "message": "Bad Request: The input data is not valid. Please check the input format and try again.",
    "timestamp": "2025-01-08T17:27:28Z"
    }
- Add testing: e.g. with pytest, see https://flask.palletsprojects.com/en/stable/testing/
- Add logging: help track/debug
- Add timestamps: help track/debug
- Validate input data: json-schema validation, e.g. using a tool like pydantic
- Separate configuration from code as environment variables: helps to switch between different environments, here e..g the flask host & port
- Add  GET method: for user-friendliness, observability and health-checking or metrics
'''

# app.py
from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load('assets/model.pickle')
scaler = joblib.load('assets/scaler.pickle')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)

    if not set(model.feature_names_in_) == set(data.keys()):
        raise ValueError(f"Invalid input. Expected: {model.feature_names_in_}, got: {data.keys()}")

    # Only processing for now is the scaling
    # Features need to be in the right order to scale it
    X = pd.DataFrame([{k: data[k] for k in scaler.feature_names_in_}])
    X = scaler.transform(X)

    prediction = model.predict(X)[0]
    assert prediction in ["B", "M"], f"Invalid raw prediction: {prediction}"
    prediction = "malignant" if prediction == 'M' else "benign"
    probability = model.predict_proba(X)[:,1][0]

    response = {"response": {"body": {"class": prediction, "probability": probability}}}
    response = jsonify(response)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)