import time
from queue import Queue
from analyzer.mythX import MythX


class Main:
    def __init__(self):
        pass

    def main(self):
        # create different queues
        new_address_q = Queue()
        report_q = Queue()
        # create different threads
        myth_x = MythX(new_address_q, report_q)
        myth_x.start()

        try:
            while True:
                time.sleep(.1)
        except KeyboardInterrupt:
            pass
        finally:
            new_address_q.put(None)
            report_q.put(None)
