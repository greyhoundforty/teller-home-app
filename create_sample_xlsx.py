#!/usr/bin/env python3
"""
Create a sample subscriptions.xlsx file for testing import functionality.
"""
from openpyxl import Workbook

# Create workbook and get active sheet
wb = Workbook()
ws = wb.active
ws.title = "Subscriptions"

# Add header row
headers = ["name", "email", "amount", "day_of_month", "frequency", "category"]
ws.append(headers)

# Add sample data
subscriptions = [
    ["Netflix", "user@example.com", 15.99, 1, "monthly", "Entertainment"],
    ["Spotify", "user@example.com", 10.99, 5, "monthly", "Entertainment"],
    ["Amazon Prime", "user@example.com", 139.00, 15, "yearly", "Subscriptions"],
    ["Adobe Creative Cloud", "work@example.com", 54.99, 20, "monthly", "Software"],
    ["Gym Membership", "user@example.com", 29.99, 10, "monthly", "Healthcare"],
    ["Internet Service", "user@example.com", 79.99, 25, "monthly", "Utilities"],
]

for sub in subscriptions:
    ws.append(sub)

# Save the file
wb.save("sample_subscriptions.xlsx")
print("✓ Created sample_subscriptions.xlsx")
