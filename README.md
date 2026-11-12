# Mosque Data Manager
## Project Overview
A Python desktop application for maintaining mosque records in SQLite and opening a selected mosque on an interactive Folium map.

## Problem Statement
Provide a small, local interface for looking up mosque information and connecting stored coordinates to a map.

## Key Features
- Add, list, and delete mosque records.
- Search by name, with approximate-name suggestions using Python's difflib.
- Update the imam name for an existing record.
- Store names, types, addresses, coordinates, and imam names.
- Generate `mosque_map.html` and open it in the default browser.
- Parameterized SQL queries for database operations.

## Technologies Used
Python 3, Tkinter/ttk, SQLite, Folium, difflib, and the standard webbrowser module.

## Architecture Overview
`MosqueDatabase` manages persistence; `MosquesManagementSystem` manages the Tkinter interface and invokes database operations. The map is generated as a local HTML file.

## Project Structure
| File | Purpose |
| --- | --- |
| `project3MMS.py` | Application entry point, GUI, database access, and map generation |
| `Mosques.db` | Included SQLite database |
| `mosque_map.html` | Included/generated map output |

## Installation
Use Python 3 with Tkinter available and a graphical desktop:
```sh
python -m venv .venv
# Activate your virtual environment, then:
python -m pip install folium
python project3MMS.py
```
On some Linux systems Tkinter is supplied separately by the operating system. Dependency versions are not locked. Setup is source-derived and was not runtime-tested during this documentation update.

## Configuration
Run from the repository root: the database and generated map paths are relative to the current working directory. Back up `Mosques.db` before modifying records. Use a separate local copy for experiments; do not commit personal records or generated maps containing private locations.

## Usage
Enter a name and type to add a record; coordinates use `latitude,longitude`. Search by name, update an imam using the record ID, or delete by ID. Enter an exact stored name before selecting Display on Map. Online map tiles require an internet connection.

## Future Improvements
- Separate GUI, persistence, and mapping into modules.
- Validate coordinate ranges and make all editable fields consistent.
- Add database tests, deletion confirmation, and repeatable dependency installation.
- Replace committed operational data with an explicitly sanitized sample.

## Author
[Albarq-CS](https://github.com/Albarq-CS)
