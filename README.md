# Wine AI

School project

Suggest user a wine based on user preferences.

## Requirements

- Python 3.7

## Installation

```bash
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

## Run project:

```
$ python main.py
```
or
```
$ python main.py --no-gui
```

## Run debug server:

In separate terminal:
```bash
$ cd remote_debugger
$ python debug_server.py
```
In `wine_ai/settings.py` set `REMOTE_DEBUGGING` to True.

## Init db from csv file (If no .db file)

```bash
$ python main.py --init-db
```

---
Looks best on KDE Plasma
