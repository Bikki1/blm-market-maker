from flask import Flask, jsonify, render_template
from mm_bot import CoinstoreMMBot
import threading
import time

app = Flask(__name__)
bot = None
bot_thread = None
bot_running = False

def run_bot():
    global bot, bot_running
    while bot_running:
        try:
            bot.run()
        except Exception as e:
            print(f"Bot error: {str(e)}")
            time.sleep(60)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start', methods=['POST'])
def start_bot():
    global bot, bot_thread, bot_running
    if not bot_running:
        try:
            bot = CoinstoreMMBot()
            bot_running = True
            bot_thread = threading.Thread(target=run_bot)
            bot_thread.daemon = True
            bot_thread.start()
            return jsonify({'status': 'Bot started successfully'})
        except Exception as e:
            return jsonify({'status': f'Error starting bot: {str(e)}'})
    return jsonify({'status': 'Bot is already running'})

@app.route('/api/stop', methods=['POST'])
def stop_bot():
    global bot_running
    if bot_running:
        bot_running = False
        time.sleep(2)  # Wait for bot to clean up
        return jsonify({'status': 'Bot stopped successfully'})
    return jsonify({'status': 'Bot is not running'})

@app.route('/api/status')
def get_status():
    global bot, bot_running
    if not bot or not bot_running:
        return jsonify({
            'running': False,
            'trend': 'neutral',
            'volatility': 0,
            'volume': 0
        })
    
    try:
        ticker = bot.get_ticker()
        trend = bot.get_market_trend()
        volatility = bot.calculate_volatility()
        
        return jsonify({
            'running': True,
            'trend': trend,
            'volatility': volatility,
            'volume': ticker['volume'] if ticker else 0
        })
    except Exception as e:
        print(f"Error getting status: {str(e)}")
        return jsonify({
            'running': True,
            'trend': 'neutral',
            'volatility': 0,
            'volume': 0
        })

@app.route('/api/balance')
def get_balance():
    global bot
    if not bot:
        return jsonify({'BLM': 0, 'USDT': 0})
    
    try:
        balance = bot.get_balance()
        return jsonify(balance or {'BLM': 0, 'USDT': 0})
    except Exception as e:
        print(f"Error getting balance: {str(e)}")
        return jsonify({'BLM': 0, 'USDT': 0})

@app.route('/api/profit_stats')
def get_profit_stats():
    global bot
    if not bot:
        return jsonify({
            'total_profit': 0,
            'trade_count': 0,
            'avg_profit_per_trade': 0
        })
    
    try:
        stats = bot.get_profit_stats()
        return jsonify(stats or {
            'total_profit': 0,
            'trade_count': 0,
            'avg_profit_per_trade': 0
        })
    except Exception as e:
        print(f"Error getting profit stats: {str(e)}")
        return jsonify({
            'total_profit': 0,
            'trade_count': 0,
            'avg_profit_per_trade': 0
        })

@app.route('/api/orders')
def get_orders():
    global bot
    if not bot:
        return jsonify([])
    
    try:
        ticker = bot.get_ticker()
        if ticker:
            buy_orders, sell_orders = bot.calculate_orders(ticker)
            all_orders = buy_orders + sell_orders
            return jsonify(all_orders)
    except Exception as e:
        print(f"Error getting orders: {str(e)}")
    
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
