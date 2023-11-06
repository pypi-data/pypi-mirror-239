#!/usr/bin/env python
# coding: utf-8

from time import ctime
from pathlib import Path
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from datetime import datetime
from dataclasses import dataclass

@dataclass
class FileProperties:
    atime: datetime
    mtime: datetime
    ctime: datetime
    size: int
    
class File:
    _DEFAULT_SALT = b'salt_^h.W#(e6-OHplcig:?6@+((8{_f2skE'
    
    def __init__(self, filepath: str|Path)-> None:
        self.filepath: Path = Path(str(filepath))

    def __str__(self) -> str:
        if props := self.properties:
            return (
                f'Name\t\t: {self.name}'
                f'\nDirectory\t: {self.parent}'
                '\nExists\t\t: True'
                f'\nAccess Time\t: {props.atime:%Y-%m-%d %H:%M:%S}'
                f'\nModified Time\t: {props.mtime:%Y-%m-%d %H:%M:%S}'
                f'\nChange Time\t: {props.ctime:%Y-%m-%d %H:%M:%S}'
                f'\nSize\t\t: {props.size/1024:.2f} KB'
            )
        else:
            return (
                f'Name        : {self.name}'
                f'\nDirectory   : {self.parent}'
                '\nExists          : False'
            )
            
    def __repr__(self) -> str:
        return f'File(filepath="{self.filepath}")'
    
    def __del__(self) -> bool:
        if self.filepath.exists():
            self.filepath.unlink()
            return True
        else:
            return False
    def __len__(self) -> int:
        """Returns size of file in Bytes"""
        if self.exists() and self.stat:
            return self.stat.st_size
        else:
            return 0
        
    def __gt__(self, other) -> bool:
        if isinstance(other, File):
            return len(self) > len(other)
        elif type(other) in (int, float):
            return len(self) > other
        else:
            raise TypeError(f"Unsupported comparison between instances of 'File' and '{other.__class__.__name__}'")  # noqa: E501

    def __lt__(self, other) -> bool:
        if isinstance(other, File):
            return len(self) < len(other)
        elif type(other) in (int, float):
            return len(self) < other
        else:
            raise TypeError(f"Unsupported comparison between instances of 'File' and '{other.__class__.__name__}'")  # noqa: E501

    def __ge__(self, other) -> bool:
        if isinstance(other, File):
            return len(self) >= len(other)
        elif type(other) in (int, float):
            return len(self) >= other
        else:
            raise TypeError(f"Unsupported comparison between instances of 'File' and '{other.__class__.__name__}'")  # noqa: E501

    def __le__(self, other) -> bool:
        if isinstance(other, File):
            return len(self) <= len(other)
        elif type(other) in (int, float):
            return len(self) <= other
        else:
            raise TypeError(f"Unsupported comparison between instances of 'File' and '{other.__class__.__name__}'")  # noqa: E501

    def __eq__(self, other) -> bool:
        """Checks Hash; If int supplied, checks size"""
        if isinstance(other, File):
            return self.hash == other.hash
        elif isinstance(other, str):
            return self.hash == other
        elif isinstance(other, int):
            return len(self) == other
        else:
            raise TypeError(f"Unsupported comparison between instances of 'File' and '{other.__class__.__name__}'")  # noqa: E501

    def __abs__(self) -> Path:
        return self.filepath.absolute()
    
    @property
    def hash(self) -> str:
        if self.filepath.exists():
            with open(self.filepath, 'rb') as f:
                _data: bytes = f.read()
            return hashlib.md5(_data).hexdigest()
        else:
            raise Exception(f"{self.filepath} does not exist.")
        
    @property
    def stat(self):
        if self.exists():
            return self.filepath.stat()
        else:
            return None
    
    @property
    def name(self) -> str:
        "Returns the filename from the current self.filepath"
        return self.filepath.name

    @property
    def parent(self) -> Path:
        "Returns the file directory from the current self.filepath"
        return self.filepath.absolute().parent
    
    @property
    def abspath(self) -> Path:
        "Returns absolute path of the current file"
        return self.filepath.absolute()
    
    def update_filename(self, new_filename:str, rename_file: bool = False) -> str:
        "Updates the filepath of the stored file"
        new_filepath = self.filepath.parent / new_filename
        if rename_file and self.exists():
            self.filepath.rename(new_filepath)
            self.filepath = new_filepath
        return self.name
    
    def is_file(self) -> bool:
        return self.filepath.is_file()

    def exists(self) -> bool:
        return self.filepath.is_file()
    
    @property
    def properties(self) -> FileProperties|None:
        """Returns a dict of properties of the file"""
        if self.stat:
            return FileProperties(
                atime=datetime.fromtimestamp(self.stat.st_atime),
                mtime=datetime.fromtimestamp(self.stat.st_mtime),
                ctime=datetime.fromtimestamp(self.stat.st_ctime),
                size=self.stat.st_size
            )
        return None
    
    def encrypt(self, key: str='') -> bytes|None:
        """Encrypts the content of the file"""
        content = self.read()
        if content:
            fernet = _generate_key(password = key, salt=self._DEFAULT_SALT)
            return fernet.encrypt(content)
        else: 
            return None
    
    def decrypt(self, key: str='') -> bytes|None:
        """Decrypts the content of the file"""
        content = self.read()
        if content:
            fernet = _generate_key(password = key, salt=self._DEFAULT_SALT)
            return fernet.decrypt(content)
        else: 
            return None
    
    def read(self) -> bytes | None:
        if self.exists() is None:
            return None
        else:
            with open(self.filepath, 'rb') as f:
                return f.read()
        
    def write(self, content: bytes) -> None:
        with open(self.filepath, 'wb') as f:
            f.write(content)

def _generate_key(password: str, salt: bytes) -> Fernet:
    """
    Generates a key from the given password and returns it.
    """
    password_bytes: bytes = bytes(password, 'utf-8')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        )
    key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
    return Fernet(key)