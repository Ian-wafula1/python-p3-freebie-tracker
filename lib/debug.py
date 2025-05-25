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
    company = freebie.company
    freebie.dev_id = dev.id
    print(freebie.dev)
    print(freebie.company)
    print(company.freebies)
    print(dev.freebies)
    print(company.devs)
    print(dev.companies)
    import ipdb; ipdb.set_trace()
