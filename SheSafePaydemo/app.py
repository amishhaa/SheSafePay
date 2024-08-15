from flask import Flask, render_template, request, redirect, url_for
import hashlib
app = Flask(__name__)

# Root route
@app.route('/')
def index():
    return redirect(url_for('user'))

# Generate a cryptographic name (hash)
def generate_cryptographic_name(user_name):
    return hashlib.sha256(user_name.encode()).hexdigest()[:10]  # Truncated to 10 characters for simplicity

# User screen (for paying)
@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        user_name = request.form['user_name']
        phone_number = request.form['phone_number']
        amount = request.form['amount']
        
        # Generate cryptographic key and get the last 4 digits of the phone number
        crypto_name = generate_cryptographic_name(user_name)
        last_four_digits = phone_number[-4:]

        # Redirect to merchant screen with payment details
        return redirect(url_for('merchant', crypto_name=crypto_name, last_four_digits=last_four_digits, amount=amount))

    return render_template('user.html')

# Merchant screen (for receiving)
@app.route('/merchant')
def merchant():
    crypto_name = request.args.get('crypto_name')
    last_four_digits = request.args.get('last_four_digits')
    amount = request.args.get('amount')
    return render_template('merchant.html', crypto_name=crypto_name, last_four_digits=last_four_digits, amount=amount)

if __name__ == '__main__':
    app.run(debug=True)

