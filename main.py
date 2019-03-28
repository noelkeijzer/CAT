from queue import Queue
from analyzer.mythX import MythX
from threading import Event

class Main:
    def __init__(self):
        pass

    def main(self):
        # create different queues
        new_address_q = Queue()
        report_q = Queue()
        stop_event = Event()
        # create different threads
        myth_x = MythX(new_address_q, report_q, stop_event)
        myth_x.start()

        try:
            stop_event.wait()
        except KeyboardInterrupt:
            pass
        finally:
            new_address_q.put(None)
            report_q.put(None)
