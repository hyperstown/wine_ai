from sqlalchemy import create_engine

# By default it uses in memory db.
# There was no info how should it be done so I leave it like this.
MEMORY = False

# Verbose SQL commands
ECHO = False 

if MEMORY:
    ENGINE = create_engine('sqlite:///:memory:', echo=ECHO)
else:
    ENGINE = create_engine("sqlite:///wines.db", echo=ECHO)