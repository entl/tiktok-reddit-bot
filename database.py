from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from settings import DATABASE_ID, DATABASE_PWD, DATABASE_LOCATION, DATABASE_NAME

Base = declarative_base()

class TrueOffMyHeart(Base):
    __tablename__ = 'trueOffMyHeart'
    __table_args__ = {'schema': 'reddit'}

    id = Column(Integer, primary_key=True)
    submission_id = Column(Integer)
    title = Column(String(255))
    content = Column(Text)

class AskReddit(Base):
    __tablename__ = 'askReddit'
    __table_args__ = {'schema': 'reddit'} 

    id = Column(Integer, primary_key=True)
    submission_id = Column(Integer)
    title = Column(String(255))
    comments = relationship("Comment")

class Comment(Base):
    __tablename__ = 'comments'
    __table_args__ = {'schema': 'reddit'} 

    id = Column(Integer, primary_key=True)
    submission = Column(Integer, ForeignKey('reddit.askReddit.id'))
    content = Column(Text)

def make_connection():
    engine = create_engine(
        f'mysql+mysqlconnector://{DATABASE_ID}:{DATABASE_PWD}@{DATABASE_LOCATION}/{DATABASE_NAME}')
    Base.metadata.create_all(engine)
    return engine

def make_session(engine):
    session_maker = sessionmaker()
    session_maker.configure(bind=engine)
    return session_maker

if __name__ == "__main__":
    engine = make_connection()
    session_maker = make_session(engine)
    session = session_maker()
    # testAskReddit = AskReddit(submission_id = '123', title = 'testTitle')
    # session.add(testAskReddit)
    # session.commit()
    testComments = [Comment(submission=1, content = 'testComment3'), 
                    Comment(submission=1, content = 'testComment4')]
    session.bulk_save_objects(testComments)
    session.commit()

    # print(session.query(AskReddit).all())
    print(session.query(Comment).all())


