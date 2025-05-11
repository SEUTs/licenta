from flask import Flask, render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import subprocess  # Used to run the Python scripts
import getMatchData
import extractData
import licenta
import json
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this!

# Simulated user database
users = {
    "saseunticnit#seuts": generate_password_hash("gelatina2002")
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
        username = (request.form['username'] + "#" + request.form['riotTag']).lower()
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
        username = (request.form['username'] + "#" + request.form['riotTag']).lower()
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



@app.route('/lastGames')
def lastGames():
    with open("puuids.json", 'r') as f:
        puuids = json.load(f)
        credentials = session['username']
        puuid = puuids.get(credentials)
        print(puuid)
        if puuid is None:
            return render_template('index.html')
        ids = licenta.GetMatchIds(puuid, 0, 20)
        previews = []
        for id in ids:
            matchFile = getMatchData.saveMatchToFile(id)
            previews.append(getMatchData.getMatchPreview(puuid, matchFile))
        return render_template('matchHistory.html', previews=previews)

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
    winner = extractData.getWinningTeamFromFile(matchFile)
    return render_template('matchDetails.html', champions=champions, kdas=kdas, builds=builds, itemNames=itemNames, matchId=matchId, skillLevelUps=skillLevelUps, winner=winner)



@app.route('/championDetails', methods=['GET'])
def championDetails():
    matchId = request.args.get("matchId")
    participantId = int(request.args.get("participant"))

    matchFile = getMatchData.saveMatchToFile(matchId)

    temporary = getMatchData.getChampionsKDAsBuilds(matchFile)
    championName = temporary[0][participantId]
    championBuild = temporary[2][participantId]
    itemNames = temporary[3][participantId]

    buildStats = {}
    with open("itemStats.json", 'r') as f:
        stats = json.load(f)
        f.close()
        for itemName in itemNames:
            for statName in stats[itemName]:
                buildStats.update({statName: buildStats.get(statName, 0) + stats[itemName][statName]})
    
    winrates = []
    with open("sample.json", 'r') as f:
        data = json.load(f)
        f.close()
        championData = data.get(championName)
        if championData is not None:
            wins = [championData[i]["wins"] for i in range(3)]
            games = [championData[i]["games"] for i in range(3)]
            winrates.append(round(sum(wins)/sum(games) * 100, 2))

            for i in range(3):
                if games[i] != 0:
                    winrates.append(round(wins[i] / games[i] * 100, 2))
                else:
                    winrates.append(-1)
        else:
            winrates = (-1, -1, -1, -1)
    print(winrates)

    championSkillLevels = extractData.getSkillLevelUps(matchFile)[participantId]
    order = ""
    skillCounter = [0, 0, 0, 0]
    for skill in championSkillLevels:
        skillCounter[skill - 1] += 1
        if skillCounter[skill - 1] == 5:
            if skill == 1:
                order += "Q > "
            if skill == 3:
                order += "E > "
            if skill == 2:
                order += "W > "
    if len(order) == 8:
        if skillCounter[0] != 5:
            order += "Q > "
        if skillCounter[2] != 5:
            order += "E > "
        if skillCounter[1] != 5:
            order += "W > "
    if order:
        order = order[:-3]

    goldPlot = licenta.generate2GoldPlot(participantId + 1)
    
    deathStats = getMatchData.getDeathStats(matchFile)[participantId + 1]

    itemsPerMinute, itemNamesPerMinute = getMatchData.getPlayerBuildPerMinute(participantId + 1, matchFile)

    enemyTeam = 1 if participantId < 6 else 0
    championRange = list(range(enemyTeam * 5 + 1, (enemyTeam+1) * 5 + 1))
    championRange.append(participantId + 1)
    championStats = getMatchData.getDamageStatsOfAll(matchFile, championRange)
    enemyChampionStats = championStats[:-1]
    playerChampionStats = championStats[-1][participantId + 1]
    
    return render_template(
        'championPage.html', 
        championName=championName, 
        championSkillLevels=championSkillLevels, 
        goldPlot=goldPlot, 
        winrates=winrates, 
        order=order,
        deathStats=deathStats,
        championBuild=championBuild,
        itemNames=itemNames,
        buildStats=buildStats,
        itemsPerMinute=itemsPerMinute,
        itemNamesPerMinute=itemNamesPerMinute,
        enemyChampionStats=enemyChampionStats,
        playerChampionStats=playerChampionStats
    )





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

@app.route('/run_script3')
def run_script3():
    subprocess.run(['python', 'deathLocations.py'])
    return "deathLocations.py has been executed!"

if __name__ == '__main__':
    app.run(debug=True)
