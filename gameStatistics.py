import output as op


def topPlayed(numberOfTopPlayed, rows):
    if numberOfTopPlayed is None:
        print('\nAll games ever played:')
        op.printOutput(rows)
    else:
        print(f'\nTop {numberOfTopPlayed} games played:')
        op.printOutput(rows[:numberOfTopPlayed])
