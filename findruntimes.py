#!/usr/bin/env python3

import datetime
import sys


def getDateTime(hour, min):
    """Create a datetime object using hour and minute values.
    All other attributes of datetime are set to current local date and time.
    """
    return datetime.datetime.now().replace(hour=hour, minute=min, second=0, microsecond=0)


def getTaskRunTimeString(inputLine, curHour, curMin):
    """Create a string containing information about command runtime.
    It takes cron style string, current hour and minute values as parameters.
    Output string contains the soonest time at which each of the commands will fire,
    whether it is today or tomorrow and name of the command. 
    """

    try:
        inMin, inHour, inTaskStr = inputLine.split(' ')

        if inMin == '*' and inHour != '*' and inHour != curHour:
            inMin = '0'
        elif inMin == '*' and (inHour == curHour or inHour == '*'):
            inMin = curMin

        if inHour == '*' and int(inMin) < int(curMin):
            inHour = str(int(curHour) + 1)
            if inHour == '24':
                inHour = '00'
        elif inHour == '*' and inMin >= curMin:
            inHour = curHour

        inDateTime = getDateTime(int(inHour), int(inMin))
        curDateTime = getDateTime(int(curHour), int(curMin))

        resultStr = inHour + ':'
        if len(inMin) == 1:
            resultStr += '0'
        resultStr += inMin + ' '

        if curDateTime > inDateTime:
            resultStr += 'tomorrow' + ' '
        else:
            resultStr += 'today' + ' '

        resultStr += inTaskStr[:-1]
        return resultStr
    except ValueError:
        print('ERROR Sorry, this line in input file is incorrect. Please check.')


def printTasksRunTime(curHour, curMin):
    """Print a string containing information about command runtime for each command in the file.
    It takes current hour and minute values as parameters.
    It reads data from input file specified as STDIN in the command line.
    File contains cron style strings.
    """

    for inputLine in sys.stdin:
        resultStr = getTaskRunTimeString(inputLine, curHour, curMin)
        if resultStr:
            print(resultStr)


def main():
    try:
        curTime = sys.argv[1]
        curHour, curMin = curTime.split(':')
        printTasksRunTime(curHour, curMin)
    except IndexError:
        print('ERROR Sorry, the arguments are incorrect. Please check.')
    except ValueError:
        print('ERROR Sorry, provided time argument is in the wrong format. Please check.')
    except Exception:
        print('ERROR Unknown error occurred')

if __name__ == "__main__":
    main()
