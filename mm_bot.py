import ccxt
import time
import random
import logging
import json
from typing import Dict, List
from datetime import datetime, timedelta
import statistics

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CoinstoreMMBot:
    def __init__(self):
        self.exchange = ccxt.coinstore({
            'apiKey': '8155c03f080c97d9928daf8ce52a5cf4',
            'secret': '46e4075f52d2e91d109f27f7efa24d01',
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot',
            }
        })
        self.symbol = 'BLM/USDT'
        self.min_spread = 0.001  # 0.1%
        self.max_spread = 0.02   # 2%
        self.min_order_size = 100  # USDT
        self.max_order_size = 1000  # USDT
        self.order_count = 5
        self.price_history = []
        self.volume_history = []
        self.profit_history = []
        self.last_rebalance = datetime.now()
        self.rebalance_interval = timedelta(hours=1)
        self.volatility_threshold = 0.02  # 2%
        self.setup_exchange()

    def setup_exchange(self):
        try:
            self.exchange.load_markets()
            logger.info(f"Connected to Coinstore Exchange")
            logger.info(f"Trading pair: {self.symbol}")
            self.fetch_initial_data()
        except Exception as e:
            logger.error(f"Error connecting to exchange: {str(e)}")
            raise

    def fetch_initial_data(self):
        """Fetch initial market data for analysis"""
        try:
            # Fetch recent trades
            trades = self.exchange.fetch_trades(self.symbol, limit=100)
            self.price_history = [trade['price'] for trade in trades]
            self.volume_history = [trade['amount'] for trade in trades]
            logger.info(f"Fetched initial market data: {len(trades)} trades")
        except Exception as e:
            logger.error(f"Error fetching initial data: {str(e)}")

    def calculate_volatility(self) -> float:
        """Calculate current market volatility"""
        if len(self.price_history) < 2:
            return 0
        returns = [
            (self.price_history[i] - self.price_history[i-1]) / self.price_history[i-1]
            for i in range(1, len(self.price_history))
        ]
        return statistics.stdev(returns) if returns else 0

    def adjust_parameters_for_volatility(self):
        """Adjust trading parameters based on market volatility"""
        volatility = self.calculate_volatility()
        if volatility > self.volatility_threshold:
            # Increase spreads and reduce order sizes in high volatility
            self.min_spread *= 1.5
            self.max_spread *= 1.5
            self.max_order_size *= 0.7
            logger.info(f"Adjusted parameters for high volatility: {volatility}")
        else:
            # Reset to default parameters in normal conditions
            self.min_spread = 0.001
            self.max_spread = 0.02
            self.max_order_size = 1000
            logger.info("Reset parameters to default values")

    def get_market_trend(self) -> str:
        """Analyze market trend using simple moving averages"""
        if len(self.price_history) < 20:
            return "neutral"
        
        short_ma = statistics.mean(self.price_history[-10:])
        long_ma = statistics.mean(self.price_history[-20:])
        
        if short_ma > long_ma * 1.005:
            return "bullish"
        elif short_ma < long_ma * 0.995:
            return "bearish"
        return "neutral"

    def get_ticker(self) -> Dict:
        try:
            ticker = self.exchange.fetch_ticker(self.symbol)
            current_price = float(ticker['last'])
            self.price_history.append(current_price)
            if len(self.price_history) > 100:
                self.price_history.pop(0)
            
            return {
                'bid': float(ticker['bid']),
                'ask': float(ticker['ask']),
                'last': current_price,
                'volume': float(ticker['quoteVolume'])
            }
        except Exception as e:
            logger.error(f"Error fetching ticker: {str(e)}")
            return None

    def calculate_dynamic_spread(self, trend: str) -> float:
        """Calculate spread based on market trend and volatility"""
        base_spread = random.uniform(self.min_spread, self.max_spread)
        volatility = self.calculate_volatility()
        
        if trend == "bullish":
            return base_spread * 1.2  # Wider spread on bullish trend
        elif trend == "bearish":
            return base_spread * 0.8  # Tighter spread on bearish trend
        return base_spread

    def calculate_orders(self, ticker: Dict) -> tuple:
        if not ticker:
            return [], []

        mid_price = (ticker['bid'] + ticker['ask']) / 2
        trend = self.get_market_trend()
        spread = self.calculate_dynamic_spread(trend)
        
        buy_orders = []
        sell_orders = []
        
        for i in range(self.order_count):
            # Adjust order sizes based on position in order book
            position_factor = 1 - (i * 0.15)  # Reduce size for orders further from mid price
            base_size = random.uniform(self.min_order_size, self.max_order_size)
            order_size = base_size * position_factor

            # Calculate prices with dynamic spreads
            buy_price = mid_price * (1 - spread * (i + 1))
            sell_price = mid_price * (1 + spread * (i + 1))
            
            buy_orders.append({
                'price': buy_price,
                'amount': order_size / buy_price,
                'side': 'buy'
            })
            
            sell_orders.append({
                'price': sell_price,
                'amount': order_size / sell_price,
                'side': 'sell'
            })
        
        logger.info(f"Generated orders - Market trend: {trend}, Spread: {spread:.4f}")
        return buy_orders, sell_orders

    def should_rebalance(self, balance: Dict) -> bool:
        """Determine if portfolio needs rebalancing"""
        if datetime.now() - self.last_rebalance < self.rebalance_interval:
            return False

        if not balance:
            return False

        blm_value = balance['BLM'] * self.price_history[-1] if self.price_history else 0
        total_value = blm_value + balance['USDT']
        blm_ratio = blm_value / total_value if total_value > 0 else 0

        return abs(blm_ratio - 0.5) > 0.1  # Rebalance if ratio deviates more than 10%

    def rebalance_portfolio(self, balance: Dict):
        """Rebalance portfolio to maintain target ratio"""
        if not balance or not self.price_history:
            return

        current_price = self.price_history[-1]
        blm_value = balance['BLM'] * current_price
        total_value = blm_value + balance['USDT']
        target_value = total_value / 2

        if blm_value > target_value:
            # Sell excess BLM
            sell_amount = (blm_value - target_value) / current_price
            try:
                self.exchange.create_market_sell_order(self.symbol, sell_amount)
                logger.info(f"Rebalancing: Sold {sell_amount:.4f} BLM")
            except Exception as e:
                logger.error(f"Rebalancing error (sell): {str(e)}")
        else:
            # Buy more BLM
            buy_amount = (target_value - blm_value) / current_price
            try:
                self.exchange.create_market_buy_order(self.symbol, buy_amount)
                logger.info(f"Rebalancing: Bought {buy_amount:.4f} BLM")
            except Exception as e:
                logger.error(f"Rebalancing error (buy): {str(e)}")

        self.last_rebalance = datetime.now()

    def place_orders(self, buy_orders: List[Dict], sell_orders: List[Dict]):
        try:
            # Cancel existing orders
            self.exchange.cancel_all_orders(self.symbol)
            
            # Place new orders
            for order in buy_orders:
                self.exchange.create_limit_buy_order(
                    self.symbol,
                    order['amount'],
                    order['price']
                )
            
            for order in sell_orders:
                self.exchange.create_limit_sell_order(
                    self.symbol,
                    order['amount'],
                    order['price']
                )
                
            logger.info(f"Successfully placed {len(buy_orders)} buy orders and {len(sell_orders)} sell orders")
        
        except Exception as e:
            logger.error(f"Error placing orders: {str(e)}")

    def get_balance(self) -> Dict:
        try:
            balance = self.exchange.fetch_balance()
            return {
                'BLM': balance.get('BLM', {}).get('free', 0),
                'USDT': balance.get('USDT', {}).get('free', 0)
            }
        except Exception as e:
            logger.error(f"Error fetching balance: {str(e)}")
            return None

    def get_profit_stats(self) -> Dict:
        """Calculate and return profit statistics"""
        try:
            trades = self.exchange.fetch_my_trades(self.symbol, limit=100)
            total_profit = sum(
                trade['amount'] * trade['price'] * (1 if trade['side'] == 'sell' else -1)
                for trade in trades
            )
            
            return {
                'total_profit': total_profit,
                'trade_count': len(trades),
                'avg_profit_per_trade': total_profit / len(trades) if trades else 0
            }
        except Exception as e:
            logger.error(f"Error calculating profit stats: {str(e)}")
            return None

    def run(self):
        while True:
            try:
                # Check balance
                balance = self.get_balance()
                if balance:
                    logger.info(f"Current balance - BLM: {balance['BLM']:.4f}, USDT: {balance['USDT']:.2f}")

                    # Check if rebalancing is needed
                    if self.should_rebalance(balance):
                        self.rebalance_portfolio(balance)

                # Adjust parameters based on market conditions
                self.adjust_parameters_for_volatility()

                # Get market data and place orders
                ticker = self.get_ticker()
                if ticker:
                    buy_orders, sell_orders = self.calculate_orders(ticker)
                    self.place_orders(buy_orders, sell_orders)

                # Calculate and log profit statistics
                profit_stats = self.get_profit_stats()
                if profit_stats:
                    logger.info(f"Profit stats: {profit_stats}")
                    self.profit_history.append(profit_stats['total_profit'])

                # Wait before next iteration
                time.sleep(60)
                
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}")
                time.sleep(60)

if __name__ == "__main__":
    bot = CoinstoreMMBot()
    bot.run()
