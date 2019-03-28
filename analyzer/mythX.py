from threading import Thread
from mythril.mythril import Mythril


class MythX(Thread):
    def __init__(self, new_address_q, report_q, event):
        Thread.__init__(self)
        self.new_address_q = new_address_q
        self.report_q = report_q
        self.event = event
        Thread.daemon = True

    def run(self):

        while not self.new_address_q.empty():
            address = self.new_address_q.get()

            if address is None:
                break

            mythril = Mythril()
            mythril.set_api_rpc('infura-ropsten')
            mythril.load_from_address(address=address)
            report = mythril.fire_lasers('bfs', address=address, contracts=mythril.contracts, max_depth=50, modules=[],
                                         transaction_count=2, enable_iprof=False)

            self.report_q.put(report)
            self.new_address_q.task_done()


if __name__ == '__main__':
    myth_x = MythX('0x3e1225be4e3839245ba76b823cfbc075b89f751a')
    myth_x.run()
