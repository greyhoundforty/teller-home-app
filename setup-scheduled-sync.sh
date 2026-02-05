#!/bin/bash
# Setup script for scheduled transaction sync

set -e

echo "Setting up scheduled transaction sync..."

# Make the sync script executable
chmod +x scheduled_sync.py

# Check if running as root (needed for systemd)
if [ "$EUID" -eq 0 ]; then
    echo "Installing systemd service and timer..."
    
    # Copy service files
    cp deployment/teller-sync.service /etc/systemd/system/
    cp deployment/teller-sync.timer /etc/systemd/system/
    
    # Reload systemd
    systemctl daemon-reload
    
    # Enable and start the timer
    systemctl enable teller-sync.timer
    systemctl start teller-sync.timer
    
    # Show status
    echo ""
    echo "✓ Systemd timer installed and started"
    echo ""
    systemctl status teller-sync.timer --no-pager
    echo ""
    echo "Next scheduled runs:"
    systemctl list-timers teller-sync.timer --no-pager
    
else
    echo "Not running as root. Setting up cron job instead..."
    
    # Create cron job (runs at 6 AM and 6 PM)
    CRON_JOB="0 6,18 * * * cd $(pwd) && $(pwd)/.venv/bin/python3 $(pwd)/scheduled_sync.py >> $(pwd)/scheduled_sync.log 2>&1"
    
    # Check if cron job already exists
    if crontab -l 2>/dev/null | grep -q "scheduled_sync.py"; then
        echo "Cron job already exists. Skipping..."
    else
        # Add cron job
        (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
        echo "✓ Cron job added (runs at 6 AM and 6 PM daily)"
    fi
    
    echo ""
    echo "Current crontab:"
    crontab -l | grep scheduled_sync.py || echo "No scheduled_sync.py cron jobs found"
fi

echo ""
echo "Setup complete!"
echo ""
echo "To manually run the sync:"
echo "  python3 scheduled_sync.py"
echo ""
echo "To view sync logs:"
echo "  tail -f scheduled_sync.log"
echo ""
echo "To check systemd timer status (if installed):"
echo "  systemctl status teller-sync.timer"
echo "  journalctl -u teller-sync.service -f"

# Made with Bob
