from events import TickEvent, QuitEvent


class CPUSpinnerController:
    def __init__(self, ev_manager, clock):
        self.ev_manager = ev_manager
        self.clock = clock
        self.keepGoing = True

    def run(self):
        while self.keepGoing:
            self.clock.tick(60)
            event = TickEvent()
            self.ev_manager.post(event)

    def notify(self, event, event_manager=None):
        if isinstance(event, QuitEvent):
            self.keepGoing = False
