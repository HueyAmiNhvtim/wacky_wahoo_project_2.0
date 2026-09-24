from sqlalchemy.orm import DeclarativeBase

# Separate the models layer from the repositories to allow separation of responsibilities
# The models describe what the data looks like, while the repositories describes how to perform operataions to get them.
class Base(DeclarativeBase):
    pass

class Videos(Base):
    pass

class Comments(Base):
    pass

class LiveComments(Base):
    pass

class Users(Base):
    pass

# TODO: Model the relationships too. We will also have to use junction tables to model some of the many-to-many relationships!