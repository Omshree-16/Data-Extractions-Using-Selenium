# Data Extractions Using Selenium

A lightweight Python project leveraging **Selenium** to automate web scraping tasks—with data extraction and manipulation using **Pandas**.

##  Overview

This repository contains scripts to scrape structured data from web pages using Selenium, and then manage the results efficiently using the powerful **Pandas** library.

##  Key Features

- **Automated Web Extraction**  
  Use Selenium WebDriver (e.g., ChromeDriver or GeckoDriver) to interact with dynamic or JavaScript-heavy websites, navigate to target URLs, and extract structured tabular or textual data.

- **Data Parsing with Pandas**  
  Load scraped data into **Pandas DataFrames** for clean-up, structuring, filtering, and exporting (e.g., to CSV), enabling seamless data manipulation and analysis.

- **Configurable & Reusable Script**  
  Easily adapt the `new_scrap.py` script for different sites by modifying the target URL and element locators—ideal for extracting course listings, tables, and other similar page elements.

- **Sample Dataset Included**  
  A sample CSV (`courses_data.csv`) is provided to demonstrate the output format and aid in testing your data workflows.

##  Getting Started

1. **Install dependencies**  
   ```bash
   pip install selenium pandas
