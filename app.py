from flask import Flask, jsonify, render_template
from scrapeTrades import get_trades
from flask import jsonify
app = Flask(__name__)

@app.route('/')
def show_trades():
    trades = get_trades()
    return render_template('trades.html', trades=trades)