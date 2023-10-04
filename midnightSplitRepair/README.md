# Midnight Split Repair

Legacy data extracted by "extractLegacy.py" and stored in "legacyData.db" were all subject to the limitation of legacy code that could not work with sessions that went past midnight. Thus, any session that goes past midnight is split into two sessions: one that starts at the original start time and ends at 23:59, and one that starts on the following day at 00:00 and ends at the original end time.

All of these sessions are identified and merged back into one.

## Usage

Place "legacyData.db" into the same directory as the code here and run "repairMidnightSplit.py". A new database file "legacyData processed.db" will be generated with all split sessions repaired.