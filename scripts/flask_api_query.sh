#!/bin/bash

# Query the API running (Not in Docker)


# Usage Examples:
# scripts/flask_api_query.sh
# OR
# bash scripts/flask_api_query.sh

# Function to display menu and get user choice
echo
echo "Welcome! This script is for testing the locally running database API."

show_menu() {
    echo
    echo "Select the API call to make, or exit the process:"
    echo "1) Fetch records by IDs"
    echo "2) Get summary using SQL"
    echo "3) Get summary using Pandas"
    echo "4) Exit"
    read -p "Enter your choice [1-4]: " choice
    return $choice
}

# Function to fetch records by IDs
fetch_records() {
    read -p "Enter comma-separated list of IDs (e.g., 1,2,3): " ids
    curl "http://localhost:8000/records?Ids=$ids"
}

# Function to get summary using SQL
summary_sql() {
    curl "http://localhost:8000/summary/sql"
}

# Function to get summary using Pandas
summary_pandas() {
    curl "http://localhost:8000/summary/pandas"
}

# Main loop
while true; do
    show_menu
    choice=$?

    case $choice in
        1) fetch_records ;;
        2) summary_sql ;;
        3) summary_pandas ;;
        4) break ;;
        *) echo "Invalid choice, please select again." ;;
    esac

    echo  # Add an empty line for spacing
done

echo "Ended process! Goodbye!"
