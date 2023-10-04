# Legacy Data Extraction

This folder contains code to extract data form a file format used for multiple years, and convert them into the format used here.

## Legacy File Format

Data was stored in .csv files titled "[year]-[month] session.csv". These files contained rows for each date with the following columns:

- Month (First row only)
- Date (Numeric, 1-31)
- Day (String, Monday - Sunday)
- Untitled columns containing sessions (String): "[Game name] [Session start time in 24h format] to [Session end time in 24h format]"

## Usage

Place legacy data in the same directory as the code here and run "extractLegacy.py". A new database "legacyData.db" in the currently used format will be produced, lacking timezone data. The legacy data was all in one timezone, so that is not a limitation for this use case.
