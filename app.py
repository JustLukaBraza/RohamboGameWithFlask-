from flask import Flask, render_template, request, jsonify
import random
import json
import os

app = Flask(__name__)


LEADERBOARD_FILE = 'leaderboard.json'

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, 'r') as f:
            return json.load(f)
    return []

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(leaderboard, f)

def get_computer_choice():
    choices = ['rock', 'paper', 'scissors']
    return random.choice(choices)

def determine_winner(player_choice, computer_choice):
    if player_choice == computer_choice:
        return "It's a tie!"
    elif (
        (player_choice == 'rock' and computer_choice == 'scissors') or
        (player_choice == 'paper' and computer_choice == 'rock') or
        (player_choice == 'scissors' and computer_choice == 'paper')
    ):
        return "You win!"
    else:
        return "Computer wins!"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    player_choice = request.json.get('choice')
    computer_choice = get_computer_choice()
    result = determine_winner(player_choice, computer_choice)
    
    return jsonify({
        'result': result,
        'computer_choice': computer_choice
    })

@app.route('/leaderboard', methods=['GET', 'POST'])
def leaderboard():
    if request.method == 'POST':
        data = request.json
        leaderboard = load_leaderboard()
        
        
        player_index = next((i for i, p in enumerate(leaderboard) if p['name'] == data['name']), -1)
        if player_index >= 0:
            leaderboard[player_index]['wins'] += data['wins']
            leaderboard[player_index]['totalGames'] += data['totalGames']
        else:
            leaderboard.append({
                'name': data['name'],
                'wins': data['wins'],
                'totalGames': data['totalGames']
            })
        
        
        leaderboard.sort(key=lambda x: x['wins'], reverse=True)
        save_leaderboard(leaderboard)
        
        return jsonify({'status': 'success'})
    
    
    leaderboard = load_leaderboard()
    return jsonify(leaderboard)

if __name__ == '__main__':
    app.run(debug=True) 