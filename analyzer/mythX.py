import datetime
from queue import Queue
from threading import Thread
from mythril.mythril import Mythril


class MythX(Thread):
    def __init__(self, new_address_q, report_q):
        Thread.__init__(self)
        self.new_address_q = new_address_q
        self.report_q = report_q
        Thread.daemon = True

    def run(self):
        while True:
            address = self.new_address_q.get()

            if address is None:
                break

            mythril = Mythril()
            mythril.set_api_rpc('infura-ropsten')
            mythril.load_from_address(address=address)
            self.log("started processing contract at address " + address)
            report = mythril.fire_lasers('bfs', address=address, contracts=mythril.contracts, max_depth=8, modules=[],
                                         transaction_count=2, enable_iprof=False)
            self.log("finished processing contract at address " + address)

            self.report_q.put((address, report.as_text()))
            self.new_address_q.task_done()

    @staticmethod
    def log(message):
        print("[CAT - {}] {}".format(datetime.datetime.now().strftime("%H:%M:%S"), message))


if __name__ == '__main__':
    address_queue = Queue()
    report_queue = Queue()
    myth_x = MythX(address_queue, report_queue)
    address_queue.put("0x3e1225be4e3839245ba76b823cfbc075b89f751a")
    address_queue.put(None)
    report = report_queue.get()
    print(report.as_text())
