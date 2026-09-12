"""Headless Scoreboard.

Keeps the exact method signatures the engine calls, but writes to bus.board
instead of Tkinter labels.  Code numbers follow the original ResultDisplay:
  0,1,2,8,9,10,11,12 -> play result text      3 -> clock     4 -> quarter
  5 -> down   6 -> yards to go   7 -> ball on   18/19 -> home/visitor score
  20/21 -> home/visitor timeouts   24 -> play call   25/26 -> offense lights
WriteLabel is only used by the engine for the OT series indicator
(grid row 6, col 9) and the two-minute-warning light (row 7, col 9).
"""
import bus

RESULT_CODES = {0, 1, 2, 8, 9, 10, 11, 12}
NAMES = {3: "clock", 4: "quarter", 5: "down", 6: "ytg", 7: "ballon",
         18: "home_score", 19: "visitor_score", 20: "home_timeouts",
         21: "visitor_timeouts", 24: "play_call", 25: "home_offense",
         26: "visitor_offense"}


class Scoreboard:
    def PlaceButton(self, *a, **k):
        return None

    def PlaceCheckBox(self, *a, **k):
        return None

    def PlaceLabel(self, *a, **k):
        return None

    def WriteLabel(self, Parent, text, width, height, fg, bg, fontsize, row,
                   column, pad, sticky):
        if (row, column) == (6, 9):
            bus.board["ot_series"] = str(text)
        elif (row, column) == (7, 9):
            bus.board["two_minute"] = (bg == "red")
        return None

    def WriteStringVarLabel(self, *a, **k):
        return None

    def UpdateScore(self, TeamScore, Score):
        TeamScore += Score
        return TeamScore

    def ResultDisplay(self, Code, Message, Subcode, Parent):
        if Code in RESULT_CODES:
            text = str(Message)
            if text:
                bus.results.append(text)
                bus.board["last_result"] = text
        elif Code in NAMES:
            bus.board[NAMES[Code]] = Message
        return None

    def ErrorMessage(self, Title, Message):
        bus.messages.append((str(Title), str(Message)))
        return None
