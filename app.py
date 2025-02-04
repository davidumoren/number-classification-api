# Import necessary libraries
from flask import Flask, request, jsonify  # Flask for creating the API
from flask_cors import CORS  # To handle CORS
import requests  # To fetch data from the Numbers API

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Helper function to check if a number is prime
def is_prime(n):
    if n < 2:  # Numbers less than 2 are not prime
        return False
    for i in range(2, int(n**0.5) + 1):  # Check divisibility up to the square root of n
        if n % i == 0:
            return False
    return True

# Helper function to check if a number is perfect
def is_perfect(n):
    if n < 2:  # Numbers less than 2 are not perfect
        return False
    sum_factors = sum(i for i in range(1, n) if n % i == 0)  # Sum of proper divisors
    return sum_factors == n

# Helper function to check if a number is an Armstrong number
def is_armstrong(n):
    digits = [int(d) for d in str(n)]  # Convert the number to a list of digits
    num_digits = len(digits)  # Number of digits
    sum_powers = sum(d ** num_digits for d in digits)  # Sum of digits raised to the power of num_digits
    return sum_powers == n

# Helper function to calculate the sum of digits
def digit_sum(n):
    return sum(int(d) for d in str(n))  # Sum of digits

# Helper function to fetch a fun fact from the Numbers API
def get_fun_fact(n):
    response = requests.get(f"http://numbersapi.com/{n}/math")  # Fetch fun fact
    return response.text if response.status_code == 200 else "No fun fact available."

# API endpoint to classify a number
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')  # Get the number from the query parameter
    
    # Input validation
    if not number or not number.lstrip('-').isdigit():  # Check if the input is a valid integer
        return jsonify({"number": number, "error": True}), 400  # Return 400 Bad Request if invalid
    
    number = int(number)  # Convert the number to an integer
    properties = []  # List to store properties of the number
    
    # Check if the number is Armstrong
    if is_armstrong(number):
        properties.append("armstrong")
    
    # Check if the number is odd or even
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    
    # Prepare the response
    response = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum(number),
        "fun_fact": get_fun_fact(number)
    }
    
    return jsonify(response), 200  # Return the response with a 200 OK status

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)  # Run the app on all available IPs and port 5000