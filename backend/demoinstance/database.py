from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, types, Column, String
import uuid
import datetime

Base = declarative_base()


class DemoData():
    Session = None

    @staticmethod
    def get_session(config):
        if DemoData.Session is not None:
            return DemoData.Session()
        connect_args = {}
        if config.database_connection.startswith('sqlite://'):
            connect_args = {'check_same_thread': False}
        engine = create_engine(
            config.database_connection,
            echo=False,
            connect_args=connect_args
        )
        Base.metadata.create_all(engine)
        Base.metadata.bind = engine
        DemoData.Session = sessionmaker(
            bind=engine, autocommit=False,
            autoflush=True, expire_on_commit=True
        )
        return DemoData.Session()


class Instance(Base):
    __tablename__ = 'instance'
    id = Column(types.Integer, primary_key=True)
    provider_id = Column(String(255), unique=True)
    name = Column(String(255))
    image_key = Column(String(255))
    status = Column(String(255), nullable=False)
    launched_at = Column(types.DATETIME)
    life_time = Column(types.Integer, nullable=False)
    token = Column(String(255), nullable=False)

    def get_dead_time(self):
        delta = (
            self.launched_at +
            datetime.timedelta(
                0, 0, 0, 0, self.life_time
            )
        ) - datetime.datetime.now()
        min = int(self._get_total_seconds(delta)/60)
        if min < 0:
            return -1
        return min

    # Python 2.6 hook
    def _get_total_seconds(self, td):
        return (
                   td.microseconds +
                   (td.seconds + td.days * 24 * 3600) *
                   1e6
               ) / 1e6


class User(Base):
    __tablename__ = 'user'
    token = Column(String(255), primary_key=True)
    login = Column(String(255), unique=True)
    last_connection = Column(types.DATETIME)

    def generate_token(self):
        self.token = str(uuid.uuid4())
        return self.token
