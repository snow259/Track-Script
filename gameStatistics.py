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

    if rows is None:
        print(name + ' was not played in the last fortnight')
    else:
        op.printOutput(rows)

    rows = dataops.returnSessionsBetweenRange(monthAgo, now, name)
    if rows is None:
        print(name + ' was not played in the last month')
    else:
        op.printOutput(rows)

    printStats(name, totalStats, fortnightStats, monthStats, yearStats)


def statsFromSessions(rows, timePeriod):
    stats = {
        'Time Period': timePeriod,
        'Time Played': dt.timedelta(seconds=0),
        'Times Played': 0,
        'Average Time': dt.timedelta(seconds=0),
    }
    if rows is not None:
        for row in rows:
            stats['count'] += 1
            stats['timePlayed'] = stats['timePlayed'] + tf.stringToTimeDelta(row['duration'])

        stats['averageTimePlayed'] = stats['timePlayed'] / stats['count']

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
    print('\n' + name + ' statistics')

    gameLife = dataops.returnSpecificGameLife(name)
    gameLife = gl.convertLifeRows(gameLife)
    # print(f"\nFirst played: {gameLife[name]['firstPlayed']}\nLast played: {gameLife[name]['lastPlayed']}")

    # print(f"\nTimes played: {totalStats['count']}")

    # print('\nTotal time:')

    # print(f"{totalStats['timePlayed']}")
    # printLargeUnitDuration(convertDurationToLargerUnits(tf.stringToTimeDelta(totalStats['timePlayed'])))

    outputRows = [totalStats, fortnightStats, monthStats, yearStats]
    op.printOutput(outputRows)


# Prints only non zero time units
def printLargeUnitDuration(largeUnitTime):
    for key in largeUnitTime.keys():
        if largeUnitTime[key] != 0:
            print(f'{largeUnitTime[key]} {key} ', end='')

    print('')
