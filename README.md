# Track-Script

I wrote this script to keep track of what games are played and for how long. All data is stored in SQLite3 databases.

Core Functionality
==================

### Opening a session

Type in the name of the game when prompted and hit enter. This opens a session, and the name and start time are written to the database

```
Enter game: gameName
```

### Closing a session

The session can be closed by typing in:

```
Enter key (close delete input): close
```

If the session has to be closed at a time different from the current time, type in:

```
Enter key (close delete input): input
```

Followed by the date and time:

```
Enter end time in format: YYYY-MM-DD HH:MM:SS
```

It can also be deleted entirely:

```
Enter key (close delete input): delete
```

### Editing a session

A session can have it's name, startTime, or endTime edited. This is done by the edit command:

```
Enter game: /edit
```

It prints out all sessions currently in the main database, then waits for the rowId of the session to be edited.

```
Enter id of session to be modified: 
```

Upon entering the rowId, it requests the quantity to be edited.

```
Enter key (name startTime endTime): 
```

### Deleting a session

A session can be deleted at any time by usage of the delete command. This is an irreversable operation.

```
Enter game: /delete
```

Like the edit command, the delete command also prints out all sessions in the main database and waits for the rowId of the session to be deleted. Multiple sessions can be deleted at once. The required rowIds should be entered separated by a comma

```
Ender ids to delete: 2
Ender ids to delete: 4, 6, 10
```

### Backups

If the script notices sessions within the main database that were opened five or more days ago, it will request a backup. This can be declined, and it will not be brought up until the script is run once again.  
If backup is run, a backup of both the main and archive databases will be performed, followed by moving all sessions from the main database to the archive database.  
It can also be run at any time by using the backup command.

```
Enter game: /backup
```

### Cancel

Almost any input can be cancelled by means of the cancel command.

```
Ender ids to delete: /cancel
Enter game:
```

Other Functions
===============

### Random Game

A game can be randomly chosen from a list provided. The list provided should be separated by commas.

```
/random game one, game two, game three
```

If no list of games are provided, one will be randomly chosen from the past five last played games.

If a single argument of an integer n is provided, a game will be randomly chosen from the last n games.

```
/random 6
```

If the provided integer is larger than the number of games played, one will be randomly chosen from any of the last played games.

### Recent

The most recently played games (default 5) can be printed out.

```
/recent
```

If more or less recently played games are needed, an integer can also be added to the command. The following prints the last 10 games played, or all games played if there aren't that many:

```
/recent 10
```

### Stats

Prints out some statistics of a game. Currently prints out the time spent in game, number of times played, and average time played for the last fortnight, month, year, and all time. Also prints out the dates between which it has been played and the current rank in terms of time played.

```
/stats name
```

### Top

Time spent in games sorted in descending order by time played followed by times played (default 15) can be viewed with the following command:

```
/top
```

A different count can be viewed by adding an integer to the command. Like with recent, the following prints out the top 10 games or all games if less than that have been played:

```
/top 10
```

The Databases
=============

Both databases used are SQLite3 databases, and are found in /Data

### Main Database

It is named mainDatabase.db, and it contains all the sessions that can be viewed, edited, and deleted from the script. Any new sessions are also added to this database.  
The database also contains tables with data for the non-core functions mentioned above.  
Backup operation is requested if this database has sessions from more than five days ago.

### Archive Database

Called archiveDatabase.db, it contains every single session that has ever been made, excluding those currently in main database. It cannot be viewed or edited, but the script can read it for functions not under the main functions.

### Timezones

Both databases currently store timezones. As this feature was added on a tight schedule, it is very much a placeholder implementation.

Currently, timezones are written to the databases in the Timezones table when a time, either startTime or endTime, is written to the database.

Both the offset from UTC in seconds and the name of the timezone for both startTime and endTime are recorded in the databases. The UTC offset picks up a negative sign if the utcoffset().days object returns a -1.

The following actions trigger a timezone write:
- Start a session
- End a session
  - By using "close"
  - By using "input"
- Delete a session (deletes entry)
- Run backup (copies to Archive Database, deletes in Main Database)

The following do not trigger a timezone write:
- Editing a session

Timezones cannot be accessed in any way by the user, and currently exists solely to record the data for a future better implementation of timezones.

Game life does not work with timezones yet. As it is a feature completely generated from existing timestamps, there will not be any errors or lost data either now, or in the future when a better implementation of timezones is added. Weird values are to be expected if working around timezones as a result, until such a time.