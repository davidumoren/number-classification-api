from flask import Flask, request, jsonify
import requests
import math
import json

app = Flask(__name__)

def is_armstrong(num):
    """Checks if a number is an Armstrong number."""
    num_str = str(num)
    n = len(num_str)
    sum_of_powers = sum(int(digit)**n for digit in num_str)
    return sum_of_powers == num

def get_number_properties(num):
    """Calculates mathematical properties of a number."""
    properties = []
    if is_armstrong(num):
      properties.append("armstrong")
    if num % 2 != 0:
      properties.append("odd")
    else:
      properties.append("even")
    digit_sum = sum(int(digit) for digit in str(num))
    return properties, digit_sum

def is_perfect(num):
    """Checks if a number is a perfect number."""
    if num <= 1:
      return False
    sum_of_divisors = 0
    for i in range(1, int(math.sqrt(num)) + 1):
       if num % i == 0:
            sum_of_divisors += i
            if i * i != num:
                sum_of_divisors += num // i
    return sum_of_divisors - num == num

def is_prime(num):
  """Checks if a number is prime."""
  if num <= 1:
        return False
  if num <= 3:
        return True
  if num % 2 == 0 or num % 3 == 0:
        return False
  i = 5
  while i * i <= num:
      if num % i == 0 or num % (i + 2) == 0:
          return False
      i = i + 6
  return True


def get_fun_fact(num):
    """Fetches a fun fact about the number from Numbers API."""
    try:
       response = requests.get(f"http://numbersapi.com/{num}/math?json")
       response.raise_for_status()
       data = response.json()
       return data.get('text')
    except requests.exceptions.RequestException as e:
       return f"Could not retrieve fun fact: {e}"

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
  """API endpoint to classify a number."""
  number = request.args.get('number')

  if number is None:
       return jsonify({"error": True, "message": "Missing 'number' parameter"}), 400

  if not number.isdigit():
       return jsonify({"number": number, "error": True, "message": "Invalid input"}), 400

  try:
        number = int(number)
        properties, digit_sum = get_number_properties(number)
        fun_fact = get_fun_fact(number)
        is_prime_val = is_prime(number)
        is_perfect_val = is_perfect(number)

        response_data = {
             "number": number,
             "is_prime": is_prime_val,
            "is_perfect": is_perfect_val,
             "properties": properties,
             "digit_sum": digit_sum,
             "fun_fact": fun_fact
        }
        return jsonify(response_data), 200
  except Exception as e:
    return jsonify({"error": True, "message": f"Error processing number: {e}"}), 500


if __name__ == '__main__':
  app.run(debug=False, host='0.0.0.0', port=5000)