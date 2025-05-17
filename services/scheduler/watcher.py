from . import schedule_process
from services.scanner.borrow_scan import scan_borrowings


def start_watching():
    schedule_process.start_test_schedule(scan_borrowings)
