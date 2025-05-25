#!/usr/bin/env python3

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
import random
from seed import seed
from models import Company, Dev, Freebie, Event

if __name__ == '__main__':
    
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    seed()
    
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
    
    print("Companies that participated:", end='\n\n')
    for company in event.companies:
        print(company.name, end=', ')
    print('\n')
    
    print('Devs that attended:', end='\n\n')
    for dev in event.devs:
        print(dev.name, end=', ')
    print('\n')
    
    print('Freebies handed out at the event:', end='\n\n')
    for freebie in event.freebies(session):
        print(freebie.name, end=', ')
    
    print('\n\n')
    
    
    
    
    print('================================ Aggregate methods ================================', end='\n\n')
    
    print(f"Freebie details: {freebie.print_details()}", end='\n\n')
    
    print('Giving freebie to a dev.')
    new_freebie= company.give_freebie(dev, 'Playstation 5', 500, session)
    print(f"Owner: {session.query(Freebie).filter(Freebie.id == new_freebie.id).first().dev.name}", end='\n\n')
    
    
    oldest_company = Company.oldest_company(session)
    print(f"The oldest company is {oldest_company.name} that was founded in {oldest_company.founding_year}", end='\n\n')
    
    print(f'{dev.name} received:')
    print(f"    Water Bottle: {dev.received_one('Water Bottle', session)}")
    print(f"    Playstation 5: {dev.received_one('Playstation 5', session)}")
    print(f"    Keyboard: {dev.received_one('Keyboard', session)}")
    print(f"    Poop: {dev.received_one('Poop', session)}")
    print('\n')
    
    print('Giving away a freebie')
    freebie_given = session.query(Freebie).filter(Freebie.name == 'Playstation 5').first()
    old_dev = freebie_given.dev
    receiving_dev = random.choice(session.query(Dev).limit(30).all())
    
    print(f"Old Dev: {freebie_given.dev}")
    old_dev.give_away(receiving_dev, freebie_given, session)
    print(f"New Dev: {freebie_given.dev}")
    
    print('\n\n')
    print('Try it out for yourself!... or don\'t. Your call really.', end='\n\n\n')
    
    import ipdb; ipdb.set_trace()
