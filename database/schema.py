from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Release(Base):
    __tablename__ = 'releases'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=255), unique=True)
    version = Column(String(length=255))

    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


engine = create_engine('sqlite:///surc.sqlite', echo=False)
Base.metadata.create_all(engine)
