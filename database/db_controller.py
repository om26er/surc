from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.schema import Release


class DBController:

    session = None

    @classmethod
    def _db(cls):
        if cls.session is None:
            cls.session = sessionmaker(bind=create_engine('sqlite:///surc.sqlite'))()
        return cls.session

    @classmethod
    def compare(cls, name, version):
        db = cls._db()
        release = db.query(Release).filter(Release.name == name).one_or_none()

        if release:
            if release.version != version:
                release.version = version
                db.commit()
                return True
        else:
            release = Release(name=name, version=version)
            db.add(release)
            db.commit()

        return False
