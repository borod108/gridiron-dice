"""Stand-in for the turtle-graphics field.  Records the ball spot on the bus."""
import bus


def DrawField():
    return None


def PlaceBall(YardLine, TeamwiththeBallFlag):
    bus.ball["yardline"] = YardLine
    bus.ball["offense_flag"] = TeamwiththeBallFlag
    return None
