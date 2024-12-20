from flask import Flask, render_template, request, redirect, url_for, flash
import random
import json
import os

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

assignments_file = "assignments.json"


# Helper function to shuffle and assign participants
def draw_names():
    shuffled = list(participants.keys())
    random.shuffle(shuffled)
    return {shuffled[i]: shuffled[(i + 1) % len(shuffled)] for i in range(len(shuffled))}


# Load existing assignments or create new ones
def load_assignments():
    if os.path.exists(assignments_file):
        with open(assignments_file, "r") as file:
            return json.load(file)
    else:
        return {}


def save_assignments(assignments):
    with open(assignments_file, "w") as file:
        json.dump(assignments, file)


# Load assignments at app start
assignments = load_assignments()


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
    global assignments

    name = request.form.get('name')
    if not name or name not in participants:
        flash("Something went wrong. Please try again!")
        return redirect(url_for('index'))

    # Check if the name already has an assigned match
    if name not in assignments:
        # Assign a match and save it
        new_assignments = draw_names()
        assignments[name] = new_assignments[name]
        save_assignments(assignments)

    # Get the stored recipient
    recipient = assignments[name]
    return render_template('result.html', name=name, recipient=recipient)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
