#!/bin/bash

# Exit on error
set -e

# Function to print messages
print_message() {
    echo "===> $1"
}

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    print_message "Please run as root (sudo)"
    exit 1
fi

# Update system
print_message "Updating system packages..."
apt-get update
apt-get upgrade -y

# Install dependencies
print_message "Installing dependencies..."
apt-get install -y python3-pip python3-venv nginx certbot python3-certbot-nginx

# Create virtual environment
print_message "Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python packages
print_message "Installing Python packages..."
pip install -r requirements.txt

# Setup environment
print_message "Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    print_message "Please edit .env file with your configuration"
    exit 1
fi

# Setup Nginx
print_message "Configuring Nginx..."
cat > /etc/nginx/sites-available/blm-bot << EOF
server {
    listen 80;
    server_name \$hostname;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

ln -sf /etc/nginx/sites-available/blm-bot /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx

# Setup systemd service
print_message "Setting up systemd service..."
cp blm-bot.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable blm-bot
systemctl start blm-bot

# Final message
print_message "Deployment complete! Please check the following:"
print_message "1. Edit .env file with your configuration"
print_message "2. Check service status: systemctl status blm-bot"
print_message "3. View logs: journalctl -u blm-bot"
print_message "4. Access web interface: http://your-server-ip:5000"
