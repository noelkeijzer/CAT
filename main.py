import sys
import time
from queue import Queue
from analyzer.mythX import MythX
from scraper.scraper import Scraper

mythril_instances = 3

class Main:
    def __init__(self):
        pass

    def main(self):
        if len(sys.argv) > 1:
            Scraper.api = sys.argv[1]
        else:
            print("You did not define an Etherscan API key.")
            exit()

        # create different queues
        new_address_q = Queue()
        report_q = Queue()
        # create different threads

        for instance in range(mythril_instances):
            myth_x = MythX(new_address_q, report_q)
            myth_x.start()

        scraper = Scraper(new_address_q)
        scraper.start()

        try:
            while True:
                time.sleep(.1)
                report = report_q.get()
                print(report.as_text())
        except KeyboardInterrupt:
            pass
        finally:
            for instance in range(mythril_instances):
                new_address_q.put(None)
            report_q.put(None)


if __name__ == '__main__':
    main = Main()
    main.main()
