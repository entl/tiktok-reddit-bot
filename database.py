from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from settings import DATABASE_USER, DATABASE_PWD, DATABASE_LOCATION, DATABASE_NAME
from exceptions import CantAddRecord, RecordNotExists, CantUpdateRecord

Base = declarative_base()


class SubmissionMixin(object):
    @classmethod
    def get_submission(cls, session, submission_id: str):
        return session.query(cls).filter(cls.submission_id == submission_id).one()

    @classmethod
    def set_uploaded(cls, session, submission_id: str):
        try:
            submission = session.query(cls).filter(
                cls.submission_id == submission_id).one()
            submission.is_uploaded = True
            session.commit()
        except Exception as e:
            session.rollback()
            raise CantUpdateRecord()


class CommentMixin(object):
    @staticmethod
    def format_comments(comments):
        comments_formatted = []
        for comment in comments:
            comments_formatted.append({"submission_id": comment.submission.id, "comment_id":comment.id, "author": comment.author.name, "content": comment.body})
        return comments_formatted

    @classmethod
    def add_comments(cls, session, comments: list) -> None:
        submission_id = comments[0]['submission_id']

        with session as session:
            try:
                existing_submission = session.query(AskReddit).filter(
                    AskReddit.submission_id == submission_id).first()
                if existing_submission is None:
                    raise RecordNotExists
                session.bulk_insert_mappings(Comment, comments)
                session.commit()
            except Exception as e:
                session.rollback()
                raise CantAddRecord(e)

    @classmethod
    def get_comments(cls, session, submission_id: str):
        return session.query(cls).filter(cls.submission_id == submission_id).all()

    @classmethod
    def set_uploaded(cls, session, submission_id: str, id: int):
        try:
            submission = session.query(cls).filter(
                and_(cls.submission_id == submission_id, cls.id == id)).one()
            submission.is_uploaded = True
            session.commit()
        except Exception as e:
            session.rollback()
            raise CantUpdateRecord()


class TrueOffMyChest(Base, SubmissionMixin):
    __tablename__ = 'trueOffMyChest'
    __table_args__ = {'schema': 'reddit'}

    submission_id = Column(String(255), primary_key=True)
    author = Column(String(255))
    title = Column(String(255))
    content = Column(Text)
    is_uploaded = Column(Boolean, default=False)

    @classmethod
    def add_submission(cls, session, submission_id: str, author: str, title: str, content: str) -> None:
        with session as session:
            try:
                existing_submission = session.query(TrueOffMyChest).filter(
                    TrueOffMyChest.submission_id == submission_id).first()
                if existing_submission is not None:
                    print("Already in database")
                    return
                submission = TrueOffMyChest(
                    submission_id=submission_id, author=author, title=title, content=content)
                session.add(submission)
                session.commit()
            except Exception as e:
                session.rollback()
                raise CantAddRecord()

    def __repr__(self) -> str:
        return f"""<Submission id: {self.submission_id}, Author: {self.author}, 
                    Title: {self.title}>, Text: {self.content[:100]}..."""


class AskReddit(Base, SubmissionMixin):
    __tablename__ = 'askReddit'
    __table_args__ = {'schema': 'reddit'}

    submission_id = Column(String(255), primary_key=True)
    author = Column(String(255))
    title = Column(String(255))
    # TODO: Is uploaded should change to true only when all comments uploaded
    is_uploaded = Column(Boolean, default=False)

    @classmethod
    def add_submission(cls, session, submission_id: str, author: str, title: str) -> None:
        with session as session:
            try:
                existing_submission = session.query(AskReddit).filter(
                    AskReddit.submission_id == submission_id).first()
                if existing_submission is not None:
                    print("Already in database")
                    return
                submission = AskReddit(
                    submission_id=submission_id, author=author, title=title)
                session.add(submission)
                session.commit()
            except Exception as e:
                session.rollback()
                raise CantAddRecord()

    def __repr__(self) -> str:
        return f"<Submission id: {self.submission_id}, Author: {self.author}, Title: {self.title}>"


class Comment(Base, CommentMixin):
    __tablename__ = 'comments'
    __table_args__ = {'schema': 'reddit'}

    comment_id = Column(String(255), primary_key=True)
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

if __name__ == "__main__":
    engine = make_connection()
    session = make_session(engine)
    AskReddit.add_submission(session, "123", "test")
    # submission = AskReddit.get_submission(session, "10kzboh")
    # comments = Comment.get_comments(session, submission.submission_id)