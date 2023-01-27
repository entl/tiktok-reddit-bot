from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from settings import DATABASE_USER, DATABASE_PWD, DATABASE_LOCATION, DATABASE_NAME
from exceptions import CantAddRecord, RecordNotExists

Base = declarative_base()


class TrueOffMyChest(Base):
    __tablename__ = 'trueOffMyChest'
    __table_args__ = {'schema': 'reddit'}

    submission_id = Column(String(255), primary_key=True)
    author = Column(String(255))
    title = Column(String(255))
    content = Column(Text)
    is_uploaded = Column(Boolean, default=False)

    # def __repr__(self) -> str:
    #     return f"""<Submission id: {self.submission_id}, Author: {self.author}, 
    #                 Title: {self.title}>, Text: {self.content[:100]}..."""


class AskReddit(Base):
    __tablename__ = 'askReddit'
    __table_args__ = {'schema': 'reddit'}

    submission_id = Column(String(255), primary_key=True)
    author = Column(String(255))
    title = Column(String(255))
    # TODO: Is uploaded should change to true only when all comments uploaded
    is_uploaded = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"<Submission id: {self.submission_id}, Author: {self.author}, Title: {self.title}>"


class Comment(Base):
    __tablename__ = 'comments'
    __table_args__ = {'schema': 'reddit'}

    id = Column(Integer, primary_key=True)
    submission_id = Column(String(255), ForeignKey(
        'reddit.askReddit.submission_id'))
    author = Column(String(255))
    content = Column(Text)
    is_uploaded = Column(Boolean, default=False)

    submission = relationship("AskReddit")

    def __repr__(self) -> str:
        return f"""<Submission id: {self.id}, Author: {self.author}, 
                    Title: {self.submission.title}>"""


def make_connection():
    engine = create_engine(
        f'mysql+mysqlconnector://{DATABASE_USER}:{DATABASE_PWD}@{DATABASE_LOCATION}/{DATABASE_NAME}')
    Base.metadata.create_all(engine)
    return engine


def make_session(engine):
    session = sessionmaker(bind=engine)
    return session()


def add_submission_TrueOffMyChest(session, submission_id: str, title: str, content: str) -> None:
    with session as session:
        try:
            existing_submission = session.query(TrueOffMyChest).filter(
                TrueOffMyChest.submission_id == submission_id).first()
            if existing_submission is not None:
                print("Already in database")
                return
            submission = TrueOffMyChest(
                submission_id=submission_id, title=title, content=content)
            session.add(submission)
            session.commit()
        except:
            session.rollback()
            raise CantAddRecord


def add_submission_askReddit(session, submission_id: str, title: str) -> None:
    with session as session:
        try:
            existing_submission = session.query(AskReddit).filter(
                AskReddit.submission_id == submission_id).first()
            if existing_submission is not None:
                print("Already in database")
                return
            submission = AskReddit(submission_id=submission_id, title=title)
            session.add(submission)
            session.commit()
        except:
            session.rollback()
            raise CantAddRecord


def add_comments_askReddit(session, comments: list) -> None:
    submission_id = comments[0]['submission_id']

    with session as session:
        try:
            existing_submission = session.query(AskReddit).filter(
                AskReddit.submission_id == submission_id).first()
            if existing_submission is None:
                raise RecordNotExists
            session.bulk_insert_mappings(Comment, comments)
            session.commit()
        except:
            session.rollback()
            raise CantAddRecord


def get_TrueOffMyChest(session, submission_id: str):
    return session.query(TrueOffMyChest).filter(TrueOffMyChest.submission_id == submission_id).first()


def get_askReddit(session, submission_id: str):
    return session.query(AskReddit).filter(AskReddit.submission_id == submission_id).first()


def get_comments(session, submission_id: str):
    return session.query(Comment).filter(Comment.submission_id == submission_id).all()

if __name__ == "__main__":
    engine = make_connection()
    session = make_session(engine)
    # add_submission_TrueOffMyChest(session, "2asf2", "testTitle22", "contentTes2t")
    # print(get_TrueOffMyChest(session, "2asf2"))
    
    # print(get_askReddit(session, '10kzboh').submission_id)
    # comments = get_comments(session, '10kzboh')
    # for comment in comments:
    #     print(comment.submission.title)
    
    # add_submission_askReddit(session=session, submission_id="10kzboh", title="testTitle2")
    # add_comments_askReddit(session, [{'submission_id': '10kzboh', 'author': 'Poorly-Drawn-Beagle', 'content': 'Thanks for being there for 15 years so we could have our questions about that guy’s wife answered'},
    #                         {'submission_id': '10kzboh','author': 'CaptinDerpI', 'content': 'Happy Birthday to the place where I find myself wondering what the fuck is wrong with people'},
    #                         {'submission_id': '10kzboh', 'author': 're_Claire', 'content': 'So much. So much is wrong.'}])