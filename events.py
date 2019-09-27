from pygame import USEREVENT, NUMEVENTS
event_ids = set(x for x in range(USEREVENT, NUMEVENTS - 1))

class TowerEvent:
    TOWERMOTION = event_ids.pop()
    TOWERDOWN = event_ids.pop()
    TOWERUP = event_ids.pop()
