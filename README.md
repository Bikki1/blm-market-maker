# Baliam (BLM) Market Making Bot

[![Deploy](https://github.com/yourusername/blm-market-maker/actions/workflows/deploy.yml/badge.svg)](https://github.com/yourusername/blm-market-maker/actions/workflows/deploy.yml)
[![codecov](https://codecov.io/gh/yourusername/blm-market-maker/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/blm-market-maker)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A professional market making bot for the Baliam token on Coinstore Exchange, featuring a modern web interface and advanced trading strategies.

## 🚀 Features

- Real-time market making with dynamic spread adjustment
- Advanced market trend analysis and volatility monitoring
- Portfolio rebalancing and risk management
- Beautiful web dashboard with real-time charts
- Comprehensive API endpoints
- Secure configuration management
- GitHub Actions CI/CD pipeline
- Docker container support
- Automated testing

## 🛠 Prerequisites

- Python 3.8 or higher
- Docker (optional)
- Git
- A Coinstore Exchange account with API access

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/blm-market-maker.git
cd blm-market-maker
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```

## ⚙️ Configuration

The bot can be configured through environment variables in the `.env` file:

- `COINSTORE_API_KEY`: Your Coinstore API key
- `COINSTORE_SECRET_KEY`: Your Coinstore API secret
- `TRADING_PAIR`: Trading pair (default: BLM/USDT)
- `MIN_SPREAD`: Minimum spread percentage (default: 0.001)
- `MAX_SPREAD`: Maximum spread percentage (default: 0.02)
- `MIN_ORDER_SIZE`: Minimum order size in USDT (default: 100)
- `MAX_ORDER_SIZE`: Maximum order size in USDT (default: 1000)
- `ORDER_COUNT`: Number of orders on each side (default: 5)

## 🚀 Deployment Options

### 1. GitHub Actions Deployment

This repository includes a GitHub Actions workflow that automatically:
- Runs tests
- Checks code quality
- Builds Docker image
- Deploys to your server

To use GitHub Actions deployment:

1. Fork this repository

2. Set up GitHub Secrets:
   - `SERVER_HOST`: Your server's IP address
   - `SERVER_USERNAME`: SSH username
   - `SERVER_SSH_KEY`: SSH private key
   - `COINSTORE_API_KEY`: Your Coinstore API key
   - `COINSTORE_SECRET_KEY`: Your Coinstore secret key

3. Push to the main branch to trigger deployment

### 2. Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d
```

### 3. Manual Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Run with Gunicorn
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=./ tests/
```

## 📊 Monitoring

1. GitHub Actions Dashboard:
   - View deployment status
   - Check test results
   - Monitor code coverage

2. Application Monitoring:
   - `/api/status` endpoint for health checks
   - Real-time dashboard metrics
   - Docker container logs

## 🔒 Security

1. Environment Variables:
   - All sensitive data stored in `.env`
   - GitHub Secrets for CI/CD
   - Docker secrets support

2. API Security:
   - Rate limiting
   - IP whitelisting
   - HTTPS enforcement

## 🔄 CI/CD Pipeline

The GitHub Actions pipeline includes:
1. Code linting (flake8)
2. Unit tests (pytest)
3. Code coverage reporting
4. Docker image building
5. Automated deployment

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 🐛 Bug Reports

Please use GitHub Issues to report bugs. Include:
1. Expected behavior
2. Actual behavior
3. Steps to reproduce
4. Error messages/logs

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Support

For support:
1. Open a GitHub Issue
2. Check existing documentation
3. Join our Discord community

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/blm-market-maker&type=Date)](https://star-history.com/#yourusername/blm-market-maker&Date)

## 📊 Repository Stats

![GitHub Stats](https://github-readme-stats.vercel.app/api?username=yourusername&show_icons=true)
