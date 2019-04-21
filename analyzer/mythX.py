import datetime
from queue import Queue
from threading import Thread
import subprocess

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

            if not isinstance(address, str):
                continue

            self.log("started processing contract at address " + address)
            try:
                result = subprocess.run(['myth', '--rpc', 'infura-ropsten', '-xa', address, '--max-depth', '12'], stdout=subprocess.PIPE, timeout=60).stdout.decode('utf-8')
                self.log("finished processing contract at address " + address)
                # if not result.startswith("The analysis was completed successfully. No issues were detected."):
                self.report_q.put((address, result))
                self.new_address_q.task_done()

            except subprocess.CalledProcessError as grepexc:
                self.log("Mythril returned with the following error: " + grepexc.output)
            except subprocess.TimeoutExpired as timeout:
                self.log("Mythril took longer than a minute to process the contract at: " + address + ". Aborting")


            # mythril = Mythril()
            # mythril.set_api_rpc('infura-ropsten')
            # mythril.load_from_address(address=address)
            # # "delegatecall", "dependence_on_predictable_vars", "deprecated_ops", "ether_thief", "exceptions", "external_calls", "integer", "multiple_sends", "suicide", "unchecked_retval"
            # report = mythril.fire_lasers('bfs', address=address, contracts=mythril.contracts, max_depth=30, modules=["integer", "unchecked_retval"],
            #                             transaction_count=2, enable_iprof=False)

    @staticmethod
    def log(message):
        print("[CAT - {}] {}".format(datetime.datetime.now().strftime("%H:%M:%S"), message))


if __name__ == '__main__':
    address_queue = Queue()
    report_queue = Queue()
    myth_x = MythX(address_queue, report_queue)
    myth_x.start()
    address_queue.put("0x34ed2cefcec1f2f789f3378ce8a2cdfcd29beb16")
    address_queue.put(None)
    address, report = report_queue.get()
    print(report)
