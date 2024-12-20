from flask import Flask, render_template, request, redirect, url_for, flash
import random

app = Flask(__name__)
app.secret_key = "secret_santa_key"


participants = [
    "FARZEEN", "ANAND", "RAMEEZ", "HAMDAN", "AARTI",
    "VISHNU", "FOUAD", "SREERAG", "THANHEEM", "SAFA",
    "OMAR", "HISHAM", "SAKINA", "MOAZ", "RITIKA", "HIROSH", "SHAH", "Vyshnav"
]

assignments = {}

# Shuffle and assign participants
def draw_names():
    shuffled = participants[:]
    random.shuffle(shuffled)
    return {shuffled[i]: shuffled[(i + 1) % len(shuffled)] for i in range(len(shuffled))}

# Assign names on app start
assignments = draw_names()

@app.route('/')
def index():
    return render_template('index.html', participants=participants)

@app.route('/reveal', methods=['POST'])
def reveal():
    name = request.form.get('name')
    if not name:
        flash("Please select your name!")
        return redirect(url_for('index'))
    recipient = assignments.get(name, "No assignment found!")
    return render_template('result.html', name=name, recipient=recipient)

if __name__ == '__main__':
    app.run(host='0.0.0.0' ,debug=True)
