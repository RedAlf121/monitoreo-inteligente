from . import schedule_process
from services.scanner.borrow_scan import start_scanner

def test():
    print("Pinchando")

def start_watching():
    schedule_process.start_test_schedule(start_scanner)
