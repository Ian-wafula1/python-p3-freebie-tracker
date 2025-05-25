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
    
    
    print('================================ Freebies ================================', end='\n\n')
    print(freebie.name)
    print(f"Dev: {freebie.dev.name}")
    print(f"Company: {freebie.company.name}")
    print(f"Freebie value: ${freebie.value}")
    print(f"Time given: {str(freebie.received_at).split('.')[0]}")
    event_name = freebie.event(session).name or "Not handed out at an event"
    print(f"Event handed out: {event_name}", end='\n\n\n')
    
    
    
    
    print('================================ Company ================================', end='\n\n')
    print('Freebies:')
    for freebie in company.freebies:
        print(freebie.name, end=', ')
    print('\n')
    
    print('Devs:')
    for dev in company.devs:
        print(dev.name, end=', ')
    print('\n')
    
    print('Events:')
    for event in company.events:
        print(event.name, end=", ")
    print('\n\n')
    
    
    
    
    print('================================ Dev ================================', end='\n\n')
    print(f'Name: {dev.name}', end='\n\n')
    print(f"Role: {dev.role}", end='\n\n')
    print("Freebies received: ")
    for freebie in dev.freebies:
        print(freebie.name, end=", ")
    print('\n')
    print("Events attended: ")
    for event in dev.events:
        print(event.name, end=", ")
    print('\n')
    print("Companies associated with:")
    for company in dev.companies:
        print(company.name, end=', ')
    print('\n\n')
    
    
    
    
    print('================================ Event ================================', end='\n\n') 
    print(f'Event Name: {event.name}', end='\n\n')
    print(f'Organiser: {event.organiser}', end='\n\n')
    print(f"Location held: {event.location}", end='\n\n')
    print(f"Event theme: {event.theme}", end='\n\n')
    print(f"Date held: {str(event.date_held).split(' ')}", end='\n\n')
    
    print("Companies that participated:")
    for company in event.companies:
        print(company.name, end=', ')
    print('\n')
    
    print('Devs that attended:')
    for dev in event.devs:
        print(dev.name, end=', ')
    print('\n')
    
    print('Freebies handed out:')
    for freebie in event.freebies(session):
        print(freebie.name, end=', ')
        
    import ipdb; ipdb.set_trace()
