import json
import re
from datetime import datetime
from typing import Optional

from ..Helpers.stringHelpers import extractCoords, findStringBetween, raplaceSubstringsTo


def timeTimestamp(time_string):
    try:
        hours, minutes, seconds = map(int, time_string.split(':'))
        timestamp = hours * 3600 + minutes * 60 + seconds
        return timestamp
    except ValueError:
        return None


def yearTimestamp(date_string):
    try:
        year, month, day = map(int, date_string.split('-'))
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            days_in_month[1] = 29  # Февраль в високосном году имеет 29 дней
        days_in_year = sum(days_in_month[:month - 1]) + day
        days_since_epoch = (year - 1970) * 365  # Дни с начала года
        days_since_epoch += sum((year - 1970) // 4 for year in range(1970, year))
        days_since_epoch -= sum((year - 1970) // 100 for year in range(1970, year))
        days_since_epoch += sum((year - 1970) // 400 for year in range(1970, year))
        timestamp = days_since_epoch * 86400 + days_in_year * 86400
        return timestamp
    except ValueError:
        return None


def buildLog(logDict, logType):
    if logDict is None:
        return None

    logDict['logType'] = logType
    return logDict


logType = {
    'beowulfAuth': 'beowulfAuth',
    'auth': 'auth',
    'action': 'action',
}


class MinetestLogParser:
    logFilepath = ''
    actionPlaceholder = 'ACTION[Server]'
    beowulfPlaceholder = '[beowulf] player'
    defaultAuthPlaceholer = 'joins game.'
    encoding = 'utf-8'
    speedOptimisation = False
    # Parsing date consumes sos many resources, need optimisation
    timestamps = {}

    # speed optimisation making table of timestamps to upspeed parsing
    def __init__(self, logFilepath, encoding='utf-8', speedOptimisation=False):
        if logFilepath != '' and logFilepath != None:
            self.logFilepath = logFilepath
        self.encoding = encoding
        self.speedOptimisation = speedOptimisation

    def read(self):
        '''Returns generator for reading parsed output for each line.'''
        for line in self.rawActionReader():
            parsedLine = self.commonLineHandler(line, self.speedOptimisation)
            if parsedLine is None:
                continue
            yield parsedLine

    def rawReader(self):
        '''Returns generator for reading raw output for each line.'''
        with open(self.logFilepath, "r", encoding=self.encoding) as file:
            for line in file:
                line = line.strip()
                if len(line) == 0:
                    continue
                yield line

    def rawActionReader(self):
        '''Returns generator for reading raw output for each action line.'''
        for line in self.rawReader():
            # first, filter logs by server action
            # 2023-10-31 13:47:20: ACTION[Server]:
            if not self.isServerActionLog(line):
                continue
            yield line

    def readAll(self):
        '''Returns list of parsed action lines'''
        logs = []
        for line in self.rawActionReader():
            res = self.commonLineHandler(line)
            if res is not None:
                logs.append(res)

    def importToLineSeparatedJson(self, newLogFilePath):
        '''Stores parsed actions lines like JSON-striings line per line to new file'''
        with open(newLogFilePath, 'w+', encoding=self.encoding) as f:
            for parsedLine in self.read():
                if parsedLine is not None:
                    f.write(json.dumps(parsedLine))

    def importToJson(self, newLogFilePath):
        '''Stores JSON array of all actions from log.'''

        with open(newLogFilePath, 'w+', encoding=self.encoding) as f:
            f.write("[")
            first_item = True
            for parsedLine in self.read():
                if parsedLine is not None:
                    if not first_item:
                        f.write(",")
                    f.write(json.dumps(parsedLine))
                    first_item = False
            f.write("]")

    @classmethod
    def commonLineHandler(cls, line: str, speedOptimisation=False) -> Optional[list]:
        '''Returns parsed line as list with action type and parsed data'''

        if cls.beowulfPlaceholder in line:
            # parse default anticheat authlog
            return buildLog(cls.parseBeowulfLine(line, speedOptimisation=speedOptimisation), logType["beowulfAuth"])

        elif cls.defaultAuthPlaceholer in line:
            # parse default auth log string
            return buildLog(cls.parseDefaultAuthLine(line, speedOptimisation=speedOptimisation), logType["auth"])

        else:
            # parse player action log string
            return buildLog(cls.parseActionLine(line, speedOptimisation=speedOptimisation), logType["action"])

    @classmethod
    def isServerActionLog(cls, line):
        '''Checks if raw line is action log'''
        if len(line) < 29:
            return False
        if line[21] != 'A' and line[28] != 'S':
            return False

        return True

    @classmethod
    def parseBeowulfLine(cls, line: str, speedOptimisation=False) -> Optional[dict]:
        '''Parses beowulf auth log with IP, formspec, protocol, lang and name'''
        line = cls.cleanActionLogString(line)

        if line is None:
            return None

        res = cls.extractTimestampAndAction(line, speedOptimisation)

        if res is not None:
            [timestamp, actionPart] = res
        else:
            return None

        try:
            rawAction = actionPart.split("[beowulf] player '", 1)
            if len(rawAction) != 2:
                print('Wrong auth string')
                print(actionPart)
                return None
            [name, other] = rawAction[1].split("' joined from ", 1)
            [ip, other] = other.split(" protocol_version: ", 1)
            [protocolVersion, other] = other.split(" formspec_version: ", 1)
            protoAndLang = other.split(" lang_code:", 1)
            formspecVersion = protoAndLang[0]
            if len(protoAndLang) == 1:
                lang = ''
            else:
                lang = protoAndLang[1].replace(" lang_code: ", '').strip()
        except Exception:
            print('Parsing error')
            print(Exception.__traceback__)
            return None
        return {
            "timestamp": timestamp,
            "name": name,
            "ip": ip,
            "protocolVersion": protocolVersion,
            "formspecVersion": formspecVersion,
            "lang": lang,
        }

    @classmethod
    def parseDefaultAuthLine(cls, line: str, speedOptimisation=False) -> Optional[dict]:
        '''Parses default Minetest auth line'''
        line = cls.cleanActionLogString(line)

        if line is None:
            return None

        res = cls.extractTimestampAndAction(line, speedOptimisation)

        if res is not None:
            [timestamp, actionPart] = res
        else:
            return None

        pattern = r"(\w+) \[([\d.]+)\] joins game\."
        match = re.search(pattern, actionPart)

        if match:
            playerName = match.group(1)
            ipAddress = match.group(2)
        else:
            return None
        return {
            "timestamp": timestamp,
            "name": playerName,
            "ip": ipAddress,
        }

    @classmethod
    def parseActionLine(cls, line, speedOptimisation=False):
        '''Parses player action line'''

        line = cls.cleanActionLogString(line)

        count = 1
        action = None
        meta_action = None
        node = None
        type = None
        name = None

        if line is None:
            return None

        lineLen = len(line)
        if lineLen < 30 or lineLen > 250:
            # print("Line so long or short for parse, ignore.")
            return None

        res = cls.extractTimestampAndAction(line, speedOptimisation)

        if res is not None:
            [timestamp, actionPart] = res
        else:
            return None
        actionPart = actionPart.strip()
        # print(actionPart)
        restricted_chars = ["<", "[", "/"]
        if actionPart[0] in restricted_chars or (actionPart[0] == 'S' and actionPart[6] == ':'):
            return None
        if actionPart[0] == 'C' and actionPart[4] == ":":
            # ignore CHAT: string
            return None

        rawAction = None
        try:
            [name, rawAction] = actionPart.split(" ", 1)
        except ValueError:
            pass
        if rawAction is None:
            return None
        rawAction = rawAction.replace('"', '')

        # many shitty code for parsing actions
        # print(rawAction[0:20])

        if rawAction[0:5] == 'digs ':
            action = 'digs'
            node = findStringBetween(rawAction, 'digs ', ' at ')
        elif rawAction[0:11] == "places node":
            action = 'places node'
            node = findStringBetween(rawAction, 'places node ', ' at ')
        elif rawAction[0] == 'p' and rawAction[1] != 'l' and 'punched ' in rawAction:
            action = 'punched'
            [name, other] = rawAction.split(' ', 1)
            typeAndNode = findStringBetween(rawAction, 'punched ', ' at ')
            if typeAndNode is None:
                type = 'player'
                node = findStringBetween(rawAction, 'player ', ' (')
            else:
                typeAndNode = typeAndNode.replace('"', '')
                [type, node] = typeAndNode.split(" ")
        elif rawAction[0] == 'a' and 'activates ' in rawAction:
            try:
                [action, node] = rawAction.split(' ')
            except Exception:
                # print('error ocurred while parsing activates log')
                # print(line)
                pass
        elif 'crafts ' in rawAction:
            action = 'crafts'
            name = findStringBetween(rawAction, 'player ', ' crafts')
            typeAndNode = findStringBetween(rawAction, 'punched ', ' at ')
            if typeAndNode is None:
                type = 'player'
                node = findStringBetween(rawAction, 'player ', ' (')
            else:
                typeAndNode = typeAndNode.replace('"', '')
                [type, node] = typeAndNode.split(" ")
        elif 'uses ' in rawAction:
            node = findStringBetween(rawAction, 'uses', ',')
            pass
        elif 'right-clicks ' in rawAction:
            action = 'right-clicks'
            typeAndNode = findStringBetween(rawAction, 'right-clicks ', ' at (')
            if typeAndNode is None:
                type = 'player'
                node = findStringBetween(rawAction, 'player ', ' (')
            elif 'object' in typeAndNode:
                type = 'LuaEntitySAO'
                node = findStringBetween(rawAction, 'LuaEntitySAO', ' at ')
            else:
                typeAndNode = typeAndNode.replace('"', '')
                [type, node] = typeAndNode.split(" ")
        elif ('takes' in rawAction) or ('moves' in rawAction):
            [action, node, other] = rawAction.split(" ", 2)
            if (action == 'takes' or action == 'moves') and "chest" in other:
                pattern = r'takes\s+([^ ]+)' if action == 'takes' else r'moves\s+([^ ]+)'
                match = re.search(pattern, rawAction)
                if match:
                    node = match.group(1)
                    if action == 'moves':
                        count = findStringBetween(rawAction, node, 'to')
                        type = findStringBetween(rawAction, 'to ', " at")
                    else:
                        count = findStringBetween(rawAction, node, 'from')
                        type = findStringBetween(rawAction, 'from ', " at")

                    if count == ' ':
                        count = 1
                    elif count is not None:
                        count = count.strip()
                else:
                    return None
        else:
            return None

        coords = None
        if ' at ' in rawAction:
            rawCoords = rawAction.split(" at ", 1)[1]
            rawCoords = rawCoords.replace('"', '')
            rawCoords = rawCoords.replace("'", '')

            # if rawCoords.count("(") > 1:
            #     print(rawCoords)
            #     coords = extractCoords(rawCoords.split(" ")[0])
            if rawCoords[0:4] == '[nod':
                coords = extractCoords(findStringBetween(rawCoords, 'node under=', 'above'))
            elif rawCoords[0] == '[' and rawCoords[4] == 'h' and rawCoords[8] == ']':
                # for [nothing]
                coords = None
            elif rawCoords[0] == '(' and rawCoords[len(rawCoords) - 1] == ')':
                coords = extractCoords(rawCoords)
            elif findStringBetween(rawCoords, "(", ")") is not None:
                coords = findStringBetween(rawCoords, "(", ")")
                if coords is not None:
                    coords = extractCoords(coords)
                else:
                    coords = None
            else:
                coords = None

            if coords is not None and len(coords) > 3:
                print("Error ocurred while parsing coordinates string")
                print(line)
        else:
            coords = None

        if node is not None:
            node = node.strip()

        return {
            "timestamp": timestamp,
            "name": name,
            "action": action,
            "meta_action": meta_action,
            "node": node,
            "count": count,
            "coords": coords,
            "type": type,
        }

    @classmethod
    def extractTimestampAndAction(cls, targetStr, speedOptimisation=False):
        '''Parses date into timestamp and raw action body'''

        # length datetime string like 2023-10-27 14:47:35:
        if len(targetStr) < 21:
            return None

        splittedTimeAndOther = targetStr.split('#')
        if len(splittedTimeAndOther) != 2:
            return None

        [timePart, actionPart] = splittedTimeAndOther

        try:

            if speedOptimisation:
                if timePart in cls.timestamps:
                    timestamp = cls.timestamps[timePart]
                else:
                    splittedTime = timePart.split(" ")
                    if splittedTime[0] in cls.timestamps:
                        dateTimestamp = cls.timestamps[splittedTime[0]]
                    else:
                        dateTimestamp = yearTimestamp(splittedTime[0])
                        cls.timestamps[splittedTime[0]] = dateTimestamp

                    timeInSec = timeTimestamp(splittedTime[1])
                    timestamp = timeInSec + dateTimestamp
                    cls.timestamps[timePart] = timestamp
            else:
                timestamp = datetime.strptime(timePart, "%Y-%m-%d %H:%M:%S").timestamp()

                # cls.timestamps[timePart] = timestamp

            # timestamp = timestamp = datetime.strptime(timePart, "%Y-%m-%d %H:%M:%S").timestamp()
        except Exception:
            print("Cant parse time from time string")
            print(f"Time string: {timePart}")
            return None
        del splittedTimeAndOther
        # [time, actionPart]
        timestamp = int(timestamp)
        return [timestamp, actionPart]

    @classmethod
    def cleanActionLogString(cls, line: str) -> str:
        '''Clean line from placeholder'''
        return line.replace(f': {cls.actionPlaceholder}: ', '#')
