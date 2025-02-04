from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Helper function to check if a number is Armstrong
def is_armstrong(n):
    digits = [int(d) for d in str(abs(int(n)))]  # Handle negative numbers
    num_digits = len(digits)
    sum_powers = sum(d ** num_digits for d in digits)
    return sum_powers == abs(int(n))

# Helper function to calculate the sum of digits
def digit_sum(n):
    return sum(int(d) for d in str(abs(int(n))))  # Handle negative numbers

# Helper function to get a fun fact using Numbers API
def get_fun_fact(n):
    response = requests.get(f"http://numbersapi.com/{n}/math")
    return response.text if response.status_code == 200 else "No fun fact available."

# Helper function to check if a number is prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Helper function to check if a number is even or odd
def is_even_or_odd(n):
    return "even" if n % 2 == 0 else "odd"

# API endpoint to classify a number
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')

    # Input validation
    if not number:
        return jsonify({"number": None, "error": True}), 400

    try:
        # Convert input to a float, then to an integer
        number_float = float(number)
        if not number_float.is_integer():
            return jsonify({"number": number, "error": True}), 400
        number_int = int(number_float)
    except ValueError:
        return jsonify({"number": number, "error": True}), 400
    
    # Initialize properties list
    properties = []

    # Check Armstrong property
    if is_armstrong(number_int):
        properties.append("armstrong")
    
    # Check if number is even or odd
    properties.append(is_even_or_odd(number_int))
    
    # Calculate digit sum
    digit_sum_value = digit_sum(number_int)

    # Get the fun fact
    fun_fact = get_fun_fact(number_int)

    # Prepare response JSON
    response = {
        "number": number_int,
        "is_prime": is_prime(number_int),
        "is_perfect": False,  # Perfect number check is not part of the current specification
        "properties": properties,
        "digit_sum": digit_sum_value,
        "fun_fact": fun_fact
    }

    return jsonify(response), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
