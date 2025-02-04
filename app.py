from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Helper function to check if a number is prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Helper function to check if a number is perfect
def is_perfect(n):
    if n < 2:
        return False
    sum_factors = sum(i for i in range(1, n) if n % i == 0)
    return sum_factors == n

# Helper function to check if a number is an Armstrong number
def is_armstrong(n):
    digits = [int(d) for d in str(abs(int(n)))]  # Handle negative numbers
    num_digits = len(digits)
    sum_powers = sum(d ** num_digits for d in digits)
    return sum_powers == abs(int(n))

# Helper function to calculate the sum of digits
def digit_sum(n):
    return sum(int(d) for d in str(abs(int(n))))  # Handle negative numbers

# Helper function to fetch a fun fact from the Numbers API
def get_fun_fact(n):
    response = requests.get(f"http://numbersapi.com/{n}/math")
    return response.text if response.status_code == 200 else "No fun fact available."

# API endpoint to classify a number
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')
    
    # Input validation
    if not number:
        return jsonify({"number": None, "error": True}), 400
    
    # Strip leading/trailing spaces and check if the input is a valid number
    number = number.strip()
    try:
        # Convert the input to a float first (to handle floating-point numbers)
        number_float = float(number)
        # Convert to int if it's a whole number (e.g., 42.0 -> 42)
        number_int = int(number_float) if number_float.is_integer() else number_float
    except ValueError:
        return jsonify({"number": number, "error": True}), 400
    
    # Initialize properties list
    properties = []
    
    # Check if the number is Armstrong (only for integers)
    if isinstance(number_int, int) and is_armstrong(number_int):
        properties.append("armstrong")
    
    # Check if the number is odd or even (only for integers)
    if isinstance(number_int, int):
        if number_int % 2 == 0:
            properties.append("even")
        else:
            properties.append("odd")
    
    # Prepare the response
    response = {
        "number": number_int,
        "is_prime": is_prime(abs(number_int)) if isinstance(number_int, int) else False,
        "is_perfect": is_perfect(abs(number_int)) if isinstance(number_int, int) else False,
        "properties": properties,  # Correctly populated with only the expected properties
        "digit_sum": digit_sum(number_int) if isinstance(number_int, int) else None,
        "fun_fact": get_fun_fact(number_int)
    }
    
    return jsonify(response), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run the app on all available IPs and port 5000
