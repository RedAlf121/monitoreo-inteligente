from dataclasses import dataclass
from enum import Enum

class FileComparisonStatus(Enum):
    EMPTY_FILE = "Empty file received"
    IDENTICAL = "Files are identical"
    WORSENED = "Change worsened the file"
    IMPROVED = "Change improved the file"

@dataclass
class FileComparisonResult:
    status: FileComparisonStatus

    def show_status_error(self):
        return self.status.value

    def is_correct(self):
        return self.status.value==FileComparisonStatus.IMPROVED




def compare_files(file_path_1: str, file_path_2: str) -> FileComparisonResult:
    return FileComparisonResult(FileComparisonStatus.IMPROVED)

