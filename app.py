# Import necessary libraries
from flask import Flask, request, jsonify  # Flask for creating the API
from flask_cors import CORS  # To handle CORS
import requests  # To fetch data from the Numbers API

app = Flask(__name__)
CORS(app)

# Helper functions remain unchanged
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if n < 2:
        return False
    sum_factors = sum(i for i in range(1, n) if n % i == 0)
    return sum_factors == n

def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    num_digits = len(digits)
    sum_powers = sum(d ** num_digits for d in digits)
    return sum_powers == n

def digit_sum(n):
    return sum(int(d) for d in str(n))

def get_fun_fact(n):
    response = requests.get(f"http://numbersapi.com/{n}/math")
    return response.text if response.status_code == 200 else "No fun fact available."

# Updated API endpoint
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number_str = request.args.get('number')
    
    # Input validation
    try:
        number = float(number_str)  # Attempt to convert to a float
    except (ValueError, TypeError):
        return jsonify({"number": number_str, "error": True, "message": "Invalid number format."}), 400
    
    properties = []

    # Check properties only for integers
    if number.is_integer():
        number = int(number)  # Convert to integer for property checks
        
        if is_armstrong(number):
            properties.append("armstrong")
        
        if number % 2 == 0:
            properties.append("even")
        else:
            properties.append("odd")

    response = {
        "number": number,
        "is_prime": is_prime(int(number)) if number.is_integer() else None,
        "is_perfect": is_perfect(int(number)) if number.is_integer() else None,
        "properties": properties,
        "digit_sum": digit_sum(int(number)) if number.is_integer() else None,
        "fun_fact": get_fun_fact(number)
    }

    return jsonify(response), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
