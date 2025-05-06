from flask import Flask, render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import subprocess  # Used to run the Python scripts
import getMatchData
import extractData

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this!

# Simulated user database
users = {
    "testuser": generate_password_hash("testpass")
}


# Route for the main page with buttons
@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return render_template('index.html')

# @app.route('/match')
# def displayMatch():
#     data = getMatchData.getChampionsKDAsBuilds()
#     champions = data[0]
#     kdas = data[1]
#     builds = data[2]
#     itemNames = data[3]
#     matchId = data[4]
#     return render_template('matchDetails.html', champions=champions, kdas=kdas, builds=builds, itemNames=itemNames, matchId=matchId)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user_password_hash = users.get(username)
        if user_password_hash is None:
            users.update({username: generate_password_hash(password)})
            print(users)
            session['username'] = username
            flash('Register successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user_password_hash = users.get(username)
        if user_password_hash and check_password_hash(user_password_hash, password):
            session['username'] = username
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        flash('Please log in to access the dashboard.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully.')
    return redirect(url_for('index'))


@app.route('/getMatch', methods=['GET'])
def search():
    query = request.args.get('query', '')  # get query string
    results = []

    if query:
        # Replace this with your real search logic
        data = ['apple', 'banana', 'grape', 'orange', 'pineapple']
        results = [item for item in data if query.lower() in item.lower()]

    return render_template('search.html', results=results)

@app.route('/searchForMatch', methods=['GET'])
def searchForMatch():
    return render_template('searchForMatch.html')

@app.route('/match', methods=['GET'])
def myMatch():
    matchId = request.args.get("matchId")
    matchFile = getMatchData.saveMatchToFile(matchId)
    data = getMatchData.getChampionsKDAsBuilds(matchFile)
    skillLevelUps = extractData.getSkillLevelUps(matchFile)
    champions = data[0]
    kdas = data[1]
    builds = data[2]
    itemNames = data[3]
    matchId = data[4]
    return render_template('matchDetails.html', champions=champions, kdas=kdas, builds=builds, itemNames=itemNames, matchId=matchId, skillLevelUps=skillLevelUps)

@app.route('/championDetails')
def championDetails():
    championName = request.args.get('championName')
    championSkillLevels = request.args.get('championSkillLevels')
    return render_template('championPage.html', championName=championName, championSkillLevels=championSkillLevels)

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
