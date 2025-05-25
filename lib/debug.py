#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie, Event

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    freebie = session.query(Freebie).first()
    dev = session.query(Dev).first()
    company = session.query(Company).first()
    event = session.query(Event).first()
    print('======== Freebies ========')
    print(freebie.dev)
    print(freebie.company, end='\n\n\n')
    
    print('======== Company ========')
    print(company.freebies)
    print(company.devs)
    print(company.events, end='\n\n\n')
    
    print('======== Dev ========')
    print(dev.freebies)
    print(dev.companies)
    print(dev.events, end='\n\n\n')
    
    print('======== Event ========') 
    print(event.companies)
    print(event.devs)
    print(event.freebies(session))
    
    import ipdb; ipdb.set_trace()
