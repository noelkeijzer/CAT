from threading import Thread
from mythril.mythril import Mythril


class MythX(Thread):
    def __init__(self, address):
        Thread.__init__(self)
        self.address = address

    def run(self):
        mythril = Mythril()
        mythril.set_api_rpc('infura-ropsten')

        report = mythril.fire_lasers('bfs', address=self.address ,contracts=mythril.contracts, address=self.address, max_depth=50, modules=[],
                                     transaction_count=2)
        pass


if __name__ == '__main__':
    myth_x = MythX('0x3e1225be4e3839245ba76b823cfbc075b89f751a')
    myth_x.run()
