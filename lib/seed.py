#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Event, Dev, Company, Freebie, Base

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session= sessionmaker(bind=engine)
    session = Session()
    
    session.query(Company).delete()
    session.query(Event).delete()
    session.query(Dev).delete()
    session.query(Freebie).delete()
    session.commit
    