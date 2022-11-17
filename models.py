from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, CheckConstraint, ForeignKey, String, Integer, create_engine
from sqlalchemy.engine import URL

Base = declarative_base()


class Week(Base):
    __tablename__ = 'week'

    id = Column(Integer, primary_key=True, autoincrement=True)
    week_number = Column(Integer, CheckConstraint("week_number > 0 AND week_number < 8"), unique=True)


class Task(Base):
    __tablename__ = "task_flask"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String)
    bug = Column(Integer)
    week = Column(Integer, ForeignKey("week.id"))


class SprintMixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {'mysql_engine': 'InnoDB'}
    __mapper_args__ = {'always_refresh': True}

    task = Column(String)
    bug = Column(Integer)


class SprintComplete(SprintMixin, Base):
    __tablename__ = "sprint_complete"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String, default="complete")
    Week = Column(Integer, ForeignKey("week.id"))


class SprintPending(SprintMixin, Base):
    __tablename__ = "sprint_pending"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String, default="pending")
    week = Column(Integer, ForeignKey('week.id'))


url = URL.create(
    "mssql+pyodbc",
    host="GGKU5DELL1920",
    database="Backlog",
    query={
        "driver": "ODBC Driver 17 for SQL Server",
        "trusted_connection": "yes",
    }
)
engine = create_engine(url, echo=True)
Base.metadata.create_all(bind=engine)
