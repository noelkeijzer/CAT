import time
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
            _, contract = mythril.load_from_address(address=address)
            report_object = mythril.fire_lasers('bfs', address=address, contracts=mythril.contracts, max_depth=50, modules=[],
                                         transaction_count=2, enable_iprof=False)

            self.report_q.put(report_object)
            self.new_address_q.task_done()
        print("test")


if __name__ == '__main__':
    mythril = Mythril()
    mythril.set_api_rpc('infura-ropsten')
    mythril.load_from_address(address="0x770f25b3346a64ba51f8b660b6ec4e87d2d5a0df")
    # mythril.load_from_bytecode("0x606060405263ffffffff7c010000000000000000000000000000000000000000000000000000000060003504166318160ddd811461005357806370a0823114610078578063a9059cbb146100b6575b600080fd5b341561005e57600080fd5b6100666100f9565b60405190815260200160405180910390f35b341561008357600080fd5b61006673ffffffffffffffffffffffffffffffffffffffff600435166100ff565b60405190815260200160405180910390f35b34156100c157600080fd5b6100e573ffffffffffffffffffffffffffffffffffffffff6004351660243561012b565b604051901515815260200160405180910390f35b60015481565b73ffffffffffffffffffffffffffffffffffffffff81166000908152602081905260409020545b919050565b73ffffffffffffffffffffffffffffffffffffffff33166000908152602081905260408120548290038190101561016157600080fd5b5073ffffffffffffffffffffffffffffffffffffffff3381166000908152602081905260408082208054859003905591841681522080548201905560015b929150505600a165627a7a723058200cc2771c6a95b013c804fef8aeb57a51b0e19fcb94d1a68ca89ba3f02ab67c1d0029")
    report_object = mythril.fire_lasers('bfs', address="0x770f25b3346a64ba51f8b660b6ec4e87d2d5a0df", contracts=mythril.contracts, max_depth=50, modules=[],
                                        transaction_count=2, verbose_report=True)
    print(report_object.as_text())
