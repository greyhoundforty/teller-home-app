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
- **Transactions** - View, search, filter, and export your complete transaction history across all accounts
- **Connect Bank** - Securely link additional bank accounts via Teller Connect

### Account Management
- 🔄 Sync data automatically or manually with the "Sync Now" button
- ✏️ Rename accounts with custom display names
- 📋 Switch between card and list view layouts
- 🏦 Support for checking, savings, credit card, and money market accounts

### Transaction Management
- 💳 View all transactions across accounts in one unified view
- 🔍 Search transactions by description with real-time filtering
- 📅 Filter by date range, amount, and specific accounts
- 📊 Sort by date, amount, or description (ascending/descending)
- 📥 Export transactions to CSV or JSON format
- 📱 Responsive design - table view on desktop, card view on mobile
- 🔄 Automatic sync twice daily (6 AM and 6 PM)
- 📈 View transaction statistics (total income, expenses, net flow)

### Payment Scheduling
- 📅 Schedule bill payments on specific days of the month
- 🔁 Mark payments as recurring (monthly, yearly) or one-time
- 📊 See the impact on your balance for each day
- ✅ Categorize payments by type (utilities, subscriptions, etc.)
- 📥 **Import subscriptions** from JSON, CSV, or Excel files
- 📧 Track subscription email addresses for easy account management

## 📥 Importing Subscriptions

Save time by importing your monthly/yearly subscriptions from a spreadsheet!

### Supported Formats

The app accepts **JSON**, **CSV**, and **Excel (.xlsx)** files with your subscription data.

**Required fields:**
- `name` - Service name (e.g., "Netflix")
- `amount` - Monthly or yearly cost
- `day_of_month` - Day the payment is due (1-31)

**Optional fields:**
- `email` - Account email address
- `frequency` - "monthly" or "yearly" (defaults to monthly)
- `category` - Subscription category

### Example Files

**CSV Format:**
```csv
name,email,amount,day_of_month,frequency,category
Netflix,user@example.com,15.99,1,monthly,Entertainment
Amazon Prime,user@example.com,139.00,15,yearly,Subscriptions
```

**JSON Format:**
```json
[
  {
    "name": "Netflix",
    "email": "user@example.com",
    "amount": 15.99,
    "day_of_month": 1,
    "frequency": "monthly",
    "category": "Entertainment"
  }
]
```

**Excel Format:** Create a spreadsheet with headers in the first row (`name`, `email`, `amount`, `day_of_month`, `frequency`, `category`) and your data in subsequent rows.

### How to Import

1. Navigate to the **Calendar** page
2. Find the **Import Subscriptions** card in the sidebar
3. Click **Choose File** and select your JSON, CSV, or Excel file
4. Click **Import File**
5. Your subscriptions will appear on the calendar automatically

The app validates all data and provides clear feedback about successful imports and any errors encountered.

## 🏗️ Tech Stack

- **Backend**: Python 3.12 with Flask
- **Database**: SQLite (development) / PostgreSQL (production)
- **API Integration**: Teller Connect for secure bank access
- **Frontend**: Vanilla JavaScript with responsive CSS
- **Task Runner**: Mise
- **Container**: Docker & Docker Compose
- **Excel Support**: openpyxl for .xlsx file parsing

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
│   ├── transactions.html # Transaction history
│   └── teller-connect.html # Bank linking
├── deployment/
│   ├── teller-sync.service # Systemd service for scheduled sync
│   └── teller-sync.timer   # Systemd timer (twice daily)
├── tests/                # Test files and debug utilities
├── scheduled_sync.py     # Scheduled transaction sync script
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

# Sync Operations
mise run sync         # Manual sync from Teller API
mise run sync-scheduled  # Run scheduled sync (for testing)
mise run sync-setup   # Setup automatic twice-daily sync
mise run sync-logs    # View scheduled sync logs

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
