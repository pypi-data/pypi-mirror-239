<!--- Heading --->
<div align="center">
  <h1>ak-file</h1>
  <p>
    A base module to manipulate files and folders
  </p>
<h4>
    <a href="https://github.com/rpakishore/ak-file/">View Demo</a>
  <span> · </span>
    <a href="https://github.com/rpakishore/ak-file">Documentation</a>
  <span> · </span>
    <a href="https://github.com/rpakishore/ak-file/issues/">Report Bug</a>
  <span> · </span>
    <a href="https://github.com/rpakishore/ak-file/issues/">Request Feature</a>
  </h4>
</div>
<br />

[![tests](https://github.com/rpakishore/ak-file/actions/workflows/test.yml/badge.svg)](https://github.com/rpakishore/ak-file/actions/workflows/test.yml)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/rpakishore/ak-file)
![GitHub last commit](https://img.shields.io/github/last-commit/rpakishore/ak-file)
<!-- Table of Contents -->
<h2>Table of Contents</h2>

- [1. About the Project](#1-about-the-project)
  - [1.1. Features](#11-features)
- [2. Getting Started](#2-getting-started)
  - [2.1. Dependencies](#21-dependencies)
  - [2.2. Installation](#22-installation)
- [3. Usage](#3-usage)
- [4. Roadmap](#4-roadmap)
- [4. License](#4-license)
- [5. Contact](#5-contact)
- [6. Acknowledgements](#6-acknowledgements)

<!-- About the Project -->
## 1. About the Project

A base project to simplify file manipulation

<!-- Features -->
### 1.1. Features

- Can sanitize filename based on windows limitaions
- Can search for and return files with specified filenames

<!-- Getting Started -->
## 2. Getting Started

### 2.1. Dependencies

The repo comes pre-compiled with all dependencies. Needs Python 3.11+

<!-- Installation -->
### 2.2. Installation

Install from pypi

```bash
pip install ak_file
```

<!-- Usage -->
## 3. Usage

```python
import ak_file import File
file = File("<path/to/file>")

file.exists() # Returns bool
file.properties() # Returns dict

file.encrypt(password = 'Some Fancy Password') # Returns bytes data
file._DEFAULT_SALT = b'SuperSecureSaltForEncryption' # Change default encryption salt
file.decrypt(password = 'Some Fancy Password') # Returns bytes data

# To sanitize filename
from ak_file import sanitizer
sanitizer.sanitize("Dirty_windows_file_name.ext", strict=False)

# Obfuscate/Unobfuscate filename with simple char shift
sanitizer.obfuscate('Filename to obfuscate') # Returns 'WzCvErDvqKFqFswLJtrKv'
sanitizer.unobfuscate('WzCvErDvqKFqFswLJtrKv') # Returns 'Filename to obfuscate'

# Search
from ak_file import SearchFolder
search = SearchFolder(folder_path="Folder\path", recurse=True)

search.extension(extension_str='py') # by extension
search.size(min_size=1024, max_size=2048) # Bytes; by size
search.regex(pattern=r'[A-Z]{3}\.py', case_sensitive=False) # By regex
search.modification_date(start_date=datetime(2023,01,01), end_date=datetime(2023,10,10))

## search by generic function
search.search(condition=lambda file: 'Alpha' in file.parent)
```

## 4. Roadmap

- [ ] Exception Handling
- [ ] File Operations
  - [ ] Adding methods to write content to files.
  - [ ] Methods for appending content to files.
  - [ ] Support for working with directories: create, remove, list contents, move, etc.
- [ ] Checksum Algorithms
- [ ] Metadata Extraction
- [ ] Support for More Encryption Options
- [ ] Context Managers
- [ ] File Comparison Methods
- [ ] Logging and Debugging
- [ ] Asynchronous I/O Support
- [ ] Serialization and Deserialization
- [ ] Support Different File Types

<!-- License -->
## 4. License

See LICENSE for more information.

<!-- Contact -->
## 5. Contact

Arun Kishore - [@rpakishore](mailto:pypi@rpakishore.co.in)

Project Link: [https://github.com/rpakishore/ak-file](https://github.com/rpakishore/ak-file)


<!-- Acknowledgments -->
## 6. Acknowledgements

- [Awesome README Template](https://github.com/Louis3797/awesome-readme-template/blob/main/README-WITHOUT-EMOJI.md)
- [Shields.io](https://shields.io/)