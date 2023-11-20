# Asynchronous Web Scraping for Dating Website Profiles

This repository contains scripts for asynchronous web scraping and data extraction from a dating website. The scripts utilize Playwright in Python to navigate pages, extract user information, and save it to CSV files for further analysis.

## Overview

The scripts perform the following key operations:

1. **Initial Data Extraction:**
    - Asynchronously navigates through pages of user profiles.
    - Extracts basic information like name, profile URL, image URL, sex, age, and last activity.

2. **Detailed Profile Scraping:**
    - For each user profile, navigates to the detailed profile page.
    - Extracts comprehensive information such as username, gender, age, location, personal preferences, and lifestyle details.

3. **CSV File Operations:**
    - Saves initial data extraction results to a CSV file.
    - Updates the CSV file with detailed profile information obtained from individual profile pages.

## Requirements

- Python
- asyncio
- Playwright
- csv

## Usage

1. **Initial Data Scraping:**
    - The script asynchronously visits each page of the user list, extracts basic user information, and stores it in a CSV file.

2. **Detailed Data Scraping:**
    - Reads the initial CSV file and for each user, asynchronously visits their detailed profile page to extract more comprehensive information.
    - Combines this detailed information with the initial data and saves it to a new CSV file.

## Setup

1. Install Playwright: `pip install playwright`
2. Install required Python packages: `pip install asyncio csv`

## Results

- The scripts provide an efficient way to scrape and compile a large dataset of user profiles from a dating website.
- The output is a comprehensive CSV file containing both basic and detailed user information, suitable for analysis or machine learning applications.
