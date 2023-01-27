from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from settings import DATABASE_USER, DATABASE_PWD, DATABASE_LOCATION, DATABASE_NAME
from exceptions import CantAddRecord

Base = declarative_base()

class TrueOffMyHeart(Base):
    __tablename__ = 'trueOffMyHeart'
    __table_args__ = {'schema': 'reddit'}

    id = Column(Integer, primary_key=True)
    submission_id = Column(String(255))
    title = Column(String(255))
    content = Column(Text)
    is_uploaded = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"<Submission id: {self.submission_id}, Title: {self.title}>"

class AskReddit(Base):
    __tablename__ = 'askReddit'
    __table_args__ = {'schema': 'reddit'} 

    id = Column(Integer, primary_key=True)
    submission_id = Column(String(255))
    title = Column(String(255))
    #TODO: Is uploaded should change to true only when all comments uploaded
    is_uploaded = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"<Submission id: {self.submission_id}, Title: {self.title}>"

class Comment(Base):
    __tablename__ = 'comments'
    __table_args__ = {'schema': 'reddit'} 

    id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, ForeignKey('reddit.askReddit.id'))
    content = Column(Text)
    is_uploaded = Column(Boolean, default=False)

    submission = relationship("AskReddit")

    def __repr__(self) -> str:
        return f"<Submission id: {self.id}, Title: {self.submission.title}>"

def make_connection():
    engine = create_engine(
        f'mysql+mysqlconnector://{DATABASE_USER}:{DATABASE_PWD}@{DATABASE_LOCATION}/{DATABASE_NAME}')
    Base.metadata.create_all(engine)
    return engine

def make_session(engine):
    session = sessionmaker(bind=engine)
    return session()

def add_submission_TrueOffMyHeart(session, submission_id: int, title: str, content: str):
    with session as session:
        try:
            existing_submission = session.query(TrueOffMyHeart).filter(TrueOffMyHeart.submission_id == submission_id).first()
            if existing_submission is not None:
                print("Already in database")
                return
            submission = TrueOffMyHeart(submission_id = submission_id, title = title, content = content)
            session.add(submission)
            session.commit()
        except:
            session.rollback()
            raise CantAddRecord


if __name__ == "__main__":
    engine = make_connection()
    session = make_session(engine)
    # add_submission_TrueOffMyHeart(session, "2asf2", "testTitle22", "contentTes2t")
    # testAskReddit = AskReddit(submission_id = 123, title = 'testTitle')
    # session.add(testAskReddit)
    # session.commit()
    # testComments = [Comment(submission=1, content = 'testComment3'), 
    #                 Comment(submission=1, content = 'testComment4')]
    # session.bulk_save_objects(testComments)
    # session.commit()

    # print(session.query(AskReddit).all())
    # print(session.query(Comment).all())


