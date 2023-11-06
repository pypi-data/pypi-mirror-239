from pathlib import Path
from typing import Generator, Callable
import re
from datetime import datetime

class SearchFolder:
    def __init__(self, folder_path: str|Path, recurse: bool) -> None:
        self.folderpath: Path = Path(str(folder_path))
        self.recurse = recurse
        if not self.folderpath.exists() or not self.folderpath.is_dir():
            raise ValueError(f"{folder_path} does not exist or is not a directory.")

    def __str__(self) -> str:
        return f"Search in the directory: {self.folderpath}, Recurse = {self.recurse}"

    def __repr__(self) -> str:
        return f"Search('{self.folderpath}', {self.recurse})"
    
    def search(self, condition: Callable[[Path], bool]) -> Generator[Path, None, None]:
        """Recursively search for files that satisfy a condition."""
        for file in self.folderpath.glob(f"{'**/' if self.recurse else ''}*"):
            if file.is_file() and condition(file):
                yield file

    def size(self, min_size: int, max_size: int) -> Generator[Path, None, None]:
        """Search for files within a specific size range."""
        return self.search(lambda file: min_size <= file.stat().st_size <= max_size)

    def modification_date(self, start_date: datetime, 
                            end_date: datetime) -> Generator[Path, None, None]:
        """Search for files modified within a specific date range."""
        return self.search(lambda file: start_date <= datetime.fromtimestamp(file.stat().st_mtime) <= end_date)  # noqa: E501
    
    def regex(self, pattern: str, 
                case_sensitive:bool=False) -> Generator[Path, None, None]:
        """Search for files in a directory that match a regex pattern."""
        if (not case_sensitive) and (not pattern.startswith("(?i)")):
            pattern = "(?i)" + pattern
        regex = re.compile(pattern)
        return self.search(lambda file: regex.search(file.name) is not None)

    def extension(self, extension_str: str) -> Generator[Path, None, None]:
        """Search for files in a directory with a specific extension."""
        return self.folderpath.glob(f"{'**/' if self.recurse else ''}*.{extension_str}")
    