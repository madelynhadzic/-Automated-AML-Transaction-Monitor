# Automated Anti-Money Laundering (AML) Transaction Monitor

## Project Overview
I built this project using **Python** and **SQL (SQLite)** to simulate how a real bank or fintech company continuously scans transaction logs. The goal is to enforce Bank Secrecy Act (BSA) compliance and catch suspicious financial patterns automatically.

## Compliance Risks Audited
The script sets up automated scans to watch out for two classic financial crime tactics:
1. **The Currency Threshold (Whale Alert)**: It flags any single cash or ledger transaction over $10,000. In a real bank, this is the limit that legally triggers a mandatory Currency Transaction Report (CTR).
2. **Transaction Structuring (Velocity Alert)**: It tracks accounts that try to stay under the radar by splitting up a large amount of money into smaller deposits (between $2,000 and $9,999) over a short period of time. 

## Database & Query Structure
The project uses a relational database with two linked tables: `customers` and `transactions`. 
* It uses **SQL Joins** to combine customer risk profiles with live transaction history.
* It uses **Aggregate Functions (`COUNT`, `SUM`)** and **`HAVING` filters** to calculate how many rapid transactions an account is making.
* If a pattern matches a money laundering risk, the script automatically generates an alert for a Suspicious Activity Report (SAR).
