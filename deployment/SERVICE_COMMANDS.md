# Systemd Service Management Commands

## Basic Commands

```bash
# Start service
systemctl start teller-home.service

# Stop service
systemctl stop teller-home.service

# Restart service
systemctl restart teller-home.service

# Reload service (after config changes)
systemctl reload teller-home.service

# Check status
systemctl status teller-home.service

# Enable (start on boot)
systemctl enable teller-home.service

# Disable (don't start on boot)
systemctl disable teller-home.service
```

## Viewing Logs

```bash
# View service logs (real-time)
journalctl -u teller-home.service -f

# View last 50 lines
journalctl -u teller-home.service -n 50

# View logs since today
journalctl -u teller-home.service --since today

# View logs since specific time
journalctl -u teller-home.service --since "2026-01-30 10:00:00"

# View application logs
tail -f /home/teller/teller-home-app/logs/access.log
tail -f /home/teller/teller-home-app/logs/error.log
```

## Troubleshooting

```bash
# Check if service is enabled
systemctl is-enabled teller-home.service

# Check if service is active
systemctl is-active teller-home.service

# View full service configuration
systemctl cat teller-home.service

# Check for service failures
systemctl --failed

# Reload systemd after editing service file
systemctl daemon-reload
systemctl restart teller-home.service
```

## After Updating Application Code

```bash
# 1. Stop the service
systemctl stop teller-home.service

# 2. Update code (git pull or copy new files)
cd /home/teller/teller-home-app
# ... update files ...

# 3. Update dependencies if needed
source venv/bin/activate
pip install -r requirements-production.txt

# 4. Restart service
systemctl start teller-home.service

# 5. Verify
systemctl status teller-home.service
```

## Monitoring Resource Usage

```bash
# Check service resource usage
systemctl status teller-home.service

# Detailed process info
ps aux | grep gunicorn

# Check open connections
ss -tulpn | grep :5001

# Check memory usage
free -h

# Check disk space
df -h
```

## Service Configuration Files

- Service file: `/etc/systemd/system/teller-home.service`
- Application directory: `/home/teller/teller-home-app/`
- Log files: `/home/teller/teller-home-app/logs/`
- Database: `/home/teller/teller-home-app/teller_home.db`
- Environment: `/home/teller/teller-home-app/.env`
