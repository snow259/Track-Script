import output as op
import databaseOperations as dataops
import datetime as dt
import timeFunctions as tf
import gameLife as gl


def topPlayed(numberOfTopPlayed, rows):
    if numberOfTopPlayed is None:
        print('\nAll games ever played:')
        op.printOutput(rows)
    else:
        print(f'\nTop {numberOfTopPlayed} games played:')
        op.printOutput(rows[:numberOfTopPlayed])


def stats(name):
    rows = dataops.returnTotalTimePlayed()
    totalStats = dict()
    for row in rows:
        if row['name'] == name:
            totalStats['Time Period'] = 'Total'
            totalStats['Time Played'] = row['timePlayed']
            totalStats['Times Played'] = row['count']
            totalStats['Average Time'] = row['averageTimePlayed']
            break

    now = dt.datetime.now()
    fortnightAgo = now - dt.timedelta(days=14)
    monthAgo = now - dt.timedelta(days=30)
    yearAgo = now - dt.timedelta(days=365)

    rows = dataops.returnSessionsBetweenRange(fortnightAgo, now, name)
    fortnightStats = statsFromSessions(rows, 'Fortnight')

    rows = dataops.returnSessionsBetweenRange(monthAgo, now, name)
    monthStats = statsFromSessions(rows, 'Month')

    rows = dataops.returnSessionsBetweenRange(yearAgo, now, name)
    yearStats = statsFromSessions(rows, 'Year')

    printStats(name, fortnightStats, monthStats, yearStats, totalStats)


def statsFromSessions(rows, timePeriod):
    stats = {
        'Time Period': timePeriod,
        'Time Played': dt.timedelta(seconds=0),
        'Times Played': 0,
        'Average Time': dt.timedelta(seconds=0),
    }
    if rows is not None:
        for row in rows:
            stats['Times Played'] += 1
            stats['Time Played'] = stats['Time Played'] + tf.stringToTimeDelta(row['duration'])

        stats['Average Time'] = stats['Time Played'] / stats['Times Played']
    
    stats['Time Played'] = tf.timeDeltaToString(stats['Time Played'])
    stats['Average Time'] = tf.timeDeltaToString(stats['Average Time'])

    return stats


# Converts duration from the database which is in hh:mm format to years, months, days, hours, minutes
def convertDurationToLargerUnits(timePlayed):
    minutes = int(timePlayed.seconds / 60)
    hours = 0
    days = timePlayed.days
    months = 0
    years = 0

    while minutes >= 60:
        hours += 1
        minutes -= 60

    while days >= 30:
        months += 1
        days -= 30

    while months >= 12:
        years += 1
        months -= 12

    largeUnitTime = {
        'years': years,
        'months': months,
        'days': days,
        'hours': hours,
        'minutes': minutes,
    }

    return largeUnitTime


def printStats(name, totalStats, fortnightStats, monthStats, yearStats):
    print('\n' + name + ' statistics\n')

    gameLife = dataops.returnSpecificGameLife(name)
    gameLife = gl.convertLifeRows(gameLife)

    topPlayedRows = dataops.returnTotalTimePlayed()
    rank = 1
    for row in topPlayedRows:
        if row['name'] == name:
            break
        else:
            rank += 1

    print(f"Rank: {rank}\n")
    print(f"Played between {tf.dateToString(gameLife[name]['firstPlayed'])} to {tf.dateToString(gameLife[name]['lastPlayed'])}\n")

    outputRows = [totalStats, fortnightStats, monthStats, yearStats]
    op.printOutput(outputRows)


# Prints only non zero time units
def printLargeUnitDuration(largeUnitTime):
    for key in largeUnitTime.keys():
        if largeUnitTime[key] != 0:
            print(f'{largeUnitTime[key]} {key} ', end='')

    print('')
