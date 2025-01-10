# Coinstore API Configuration
COINSTORE_API_KEY = "8155c03f080c97d9928daf8ce52a5cf4"
COINSTORE_SECRET_KEY = "46e4075f52d2e91d109f27f7efa24d01"
ALLOWED_IPS = ["36.252.255.30", "2400:9500:4008:36d1:48a1:3c41:8e9e:57c2"]

# Token Configuration
TOKEN_SYMBOL = "BLM"
TOKEN_CONTRACT = "0x7F7800f193F94e448e5Dd8a67899b06227757Fb4"
TOKEN_NAME = "Baliam"
TRADING_PAIR = "BLM/USDT"

# Market Making Parameters
MIN_SPREAD = 0.001  # 0.1%
MAX_SPREAD = 0.02   # 2%
MIN_ORDER_SIZE = 100  # Minimum order size in USDT
MAX_ORDER_SIZE = 1000  # Maximum order size in USDT
ORDER_COUNT = 5  # Number of orders on each side
VOLUME_TARGET = 10000  # Daily volume target in USDT
REBALANCE_THRESHOLD = 0.1  # 10% deviation triggers rebalance
