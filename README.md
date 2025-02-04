# Number Classification API

This API classifies a number and returns its mathematical properties along with a fun fact.

# How to Use
1. Clone the repository:
   
   git clone (https://github.com/davidumoren/number-classification-api)

2. Run the API locally:

python app.py

3. Test the API:

Example request: http://localhost:5000/api/classify-number?number=371

Example response:


{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}

4. Deployment
The API is deployed on Render. You can access it here:

Public URL: https://number-classification-api.onrender.com