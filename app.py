from flask import Flask, render_template, request, redirect, url_for, flash
import random

app = Flask(__name__)
app.secret_key = "secret_santa_key"

# Participants and their secret passwords
participants = {
    "FARZEEN": "far123", "ANAND": "ana456", "RAMEEZ": "ram789",
    "HAMDAN": "ham101", "AARTI": "aar202", "VISHNU": "vis303",
    "FOUAD": "fou404", "SREERAG": "sre505", "THANHEEM": "tha606",
    "SAFA": "saf707", "OMAR": "oma808", "HISHAM": "his909",
    "SAKINA": "sak010", "MOAZ": "moa020", "RITIKA": "rit030",
    "HIROSH": "hir040", "SHAH": "sha050", "Vyshnav": "vys060"
}

# Shuffle and assign participants
def draw_names():
    shuffled = list(participants.keys())
    random.shuffle(shuffled)
    return {shuffled[i]: shuffled[(i + 1) % len(shuffled)] for i in range(len(shuffled))}

# Assign names on app start
assignments = draw_names()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    password = request.form.get('password')
    if not password:
        flash("Please enter your secret password!")
        return redirect(url_for('index'))
    
    # Find the participant associated with the password
    name = next((key for key, value in participants.items() if value == password), None)
    
    if not name:
        flash("Invalid password. Please try again!")
        return redirect(url_for('index'))
    
    # If password matches, display the name and allow to reveal
    return render_template('verify.html', name=name)

@app.route('/reveal', methods=['POST'])
def reveal():
    name = request.form.get('name')
    if not name or name not in assignments:
        flash("Something went wrong. Please try again!")
        return redirect(url_for('index'))
    
    # Get the recipient for the participant
    recipient = assignments[name]
    return render_template('result.html', name=name, recipient=recipient)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
