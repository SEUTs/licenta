from flask import Flask, render_template
import subprocess  # Used to run the Python scripts

app = Flask(__name__)

# Route for the main page with buttons
@app.route('/')
def index():
    return render_template('index.html')

# Route to run script1
@app.route('/run_script1')
def run_script1():
    subprocess.run(['python', 'licenta.py'])
    return "licenta.py has been executed!"

# Route to run script2
@app.route('/run_script2')
def run_script2():
    subprocess.run(['python', 'deathLocations.py'])
    return "deathLocations.py has been executed!"

if __name__ == '__main__':
    app.run(debug=True)
