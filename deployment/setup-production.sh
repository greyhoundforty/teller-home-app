#!/bin/bash
# Production Setup Script for Teller Home App on Proxmox LXC
# Run as root

set -e

echo "🚀 Teller Home App - Production Setup"
echo "======================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run as root"
    exit 1
fi

# Create teller user if doesn't exist
if id "teller" &>/dev/null; then
    echo "✅ User 'teller' already exists"
else
    echo "👤 Creating user 'teller'..."
    useradd -m -s /bin/bash teller
    echo "✅ User created"
fi

# Move app from root to teller's home (if running from /root)
if [ -d "/root/teller-home-app" ] && [ ! -d "/home/teller/teller-home-app" ]; then
    echo "📦 Moving app to /home/teller/teller-home-app..."
    mkdir -p /home/teller/teller-home-app
    cp -r /root/teller-home-app/* /home/teller/teller-home-app/
    cp /root/teller-home-app/.env /home/teller/teller-home-app/ 2>/dev/null || echo "⚠️  .env not found in /root"
    chown -R teller:teller /home/teller/teller-home-app
    echo "✅ App moved"
elif [ -d "/home/teller/teller-home-app" ]; then
    echo "✅ App already in /home/teller/teller-home-app"
    chown -R teller:teller /home/teller/teller-home-app
else
    echo "❌ App directory not found in /root/teller-home-app"
    exit 1
fi

# Create logs directory
echo "📝 Creating logs directory..."
mkdir -p /home/teller/teller-home-app/logs
chown teller:teller /home/teller/teller-home-app/logs
echo "✅ Logs directory created"

# Create systemd service
echo "⚙️  Creating systemd service..."
cat > /etc/systemd/system/teller-home.service << 'EOF'
[Unit]
Description=Teller Home Finance App
After=network.target

[Service]
Type=simple
User=teller
Group=teller
WorkingDirectory=/home/teller/teller-home-app

Environment="PATH=/home/teller/teller-home-app/venv/bin"
Environment="FLASK_ENV=production"

ExecStart=/home/teller/teller-home-app/venv/bin/gunicorn \
    --bind 0.0.0.0:5001 \
    --workers 2 \
    --timeout 120 \
    --access-logfile /home/teller/teller-home-app/logs/access.log \
    --error-logfile /home/teller/teller-home-app/logs/error.log \
    --log-level info \
    app:app

Restart=always
RestartSec=10

NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF
echo "✅ Service file created"

# Reload systemd
echo "🔄 Reloading systemd..."
systemctl daemon-reload
echo "✅ Systemd reloaded"

# Enable service
echo "🔧 Enabling service to start on boot..."
systemctl enable teller-home.service
echo "✅ Service enabled"

# Start service
echo "🚀 Starting service..."
systemctl start teller-home.service
sleep 2

# Check status
echo ""
echo "📊 Service Status:"
systemctl status teller-home.service --no-pager || true

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "  1. Check status: systemctl status teller-home.service"
echo "  2. View logs: journalctl -u teller-home.service -f"
echo "  3. Access app: http://$(hostname -I | awk '{print $1}'):5001"
echo ""
echo "📚 Useful commands:"
echo "  - Restart: systemctl restart teller-home.service"
echo "  - Stop: systemctl stop teller-home.service"
echo "  - Logs: tail -f /home/teller/teller-home-app/logs/access.log"
echo ""
