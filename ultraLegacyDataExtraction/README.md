# Ultra Legacy Data Extraction

Terrible title for an even older data format used prior to the legacy format. This code extracts that and attempts to convert it to the current format. Data files are all .csv files titled "[year]-[month].csv".

## File Format

This file format had named columns for each of the following:

- Month (first row only)
- Date (numeric, 1-31)
- Day (string, Monday-Sunday)
- One column for each game played (string): "[hours without leading 0]h:[minutes]m"

## Usage

Place the old data files in the same directory as the code and run "extractUltraLegacy.py". A new database "ultraLegacyData.db" will be produced. The data in the legacy files lack session times and contain only the duration a game has been played over the entire day. Thus, all sessions are assumed to start at 00:00 and end at 00:00 + duration.