""" Create tables """

from .settings import ENGINE as engine
from .models import Base

def migrate():
    """ Migrate models to database """
    Base.metadata.create_all(engine)