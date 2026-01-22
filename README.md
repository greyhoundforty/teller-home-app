# Teller Home App

A beautiful, full-featured financial management application that securely connects to your bank accounts via Teller, providing real-time balance tracking, transaction history, bill payment scheduling, and weekly financial forecasts.

## 🎯 What This App Does

**Teller Home App** helps you manage your finances in one unified dashboard by connecting directly to your real bank accounts. Instead of logging into multiple banking portals, you get a single, beautiful interface showing:

- **📊 Dashboard**: View all your account balances at a glance, with custom naming so you can distinguish between "My Chase" and "Wife's Chase"
- **📅 Calendar**: Schedule and track bill payments month by month, with projected daily balances showing the impact of your payments
- **🏦 Bank Integration**: Securely connect via Teller Connect - no passwords shared, just read-only access to your accounts
- **💾 Smart Storage**: All data is yours, stored locally or in your own database

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Your bank login credentials (for Teller Connect)

### Quick Start

```bash
# Install dependencies
mise run install

# Initialize the database
mise run db-init

# Start the app
mise run dev

# Open in your browser
open http://localhost:5001
```

### Connect Your First Bank Account
1. Navigate to the "Connect Bank" tab
2. Select your environment (Development for real banks, Sandbox for testing)
3. Follow the Teller Connect flow to authorize access to your accounts
4. Your accounts and balances will sync automatically

## ✨ Features

### Core Pages
- **Dashboard** - View all accounts with real-time balances, custom names for each account, and net worth calculation
- **Calendar** - Schedule recurring or one-time payments, see projected balances for each day based on upcoming bills
- **Connect Bank** - Securely link additional bank accounts via Teller Connect

### Account Management
- 🔄 Sync data automatically or manually with the "Sync Now" button
- ✏️ Rename accounts with custom display names
- 📋 Switch between card and list view layouts
- 🏦 Support for checking, savings, credit card, and money market accounts

### Payment Scheduling
- 📅 Schedule bill payments on specific days of the month
- 🔁 Mark payments as recurring (monthly) or one-time
- 📊 See the impact on your balance for each day
- ✅ Categorize payments by type (utilities, subscriptions, etc.)

## 🏗️ Tech Stack

- **Backend**: Python 3.12 with Flask
- **Database**: SQLite (development) / PostgreSQL (production)
- **API Integration**: Teller Connect for secure bank access
- **Frontend**: Vanilla JavaScript with responsive CSS
- **Task Runner**: Mise
- **Container**: Docker & Docker Compose

## 📁 Project Structure

```
teller-home-app/
├── app.py                 # Main Flask application
├── src/
│   ├── models.py         # SQLAlchemy ORM models
│   ├── teller_client.py  # Teller API integration
│   └── sync_service.py   # Data synchronization
├── static/
│   ├── index.html        # Home page
│   ├── dashboard.html    # Account balances & overview
│   ├── calendar.html     # Payment scheduling
│   └── teller-connect.html # Bank linking
├── tests/                # Test files and debug utilities
├── teller_home.db        # SQLite database
└── mise.toml             # Task definitions
```

## 📝 Available Commands

```bash
# Database
mise run db-init      # Initialize database schema
mise run db-reset     # Clear and reinitialize

# Development
mise run dev          # Start development server

# Testing & Quality
mise run test         # Run test suite
mise run test-cov     # Run tests with coverage
mise run lint         # Check code formatting
mise run format       # Auto-format code

# Database Management
mise run backup-restart  # Backup database and restart app
```

## 🔐 Security

- All bank connections use Teller's secure OAuth flow - we never see your passwords
- Data is stored locally in your database
- The app runs on your machine by default
- No data is sent to external servers (except Teller for authentication)

## 📚 Documentation

For more detailed information:
- See `QUICKSTART.md` for step-by-step setup
- Check `SETUP.md` for advanced configuration
- Review API endpoints in `DASHBOARD_CALENDAR_GUIDE.md`

## 🤝 Contributing

To improve the app:
1. Test your changes thoroughly
2. Run `mise run lint` to check code quality
3. Add tests for new features in `tests/`
4. Update this README if adding new functionality

## 📄 License

MIT
