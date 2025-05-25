#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Event, Dev, Company, Freebie, Base
from faker import Faker
from datetime import datetime
import random
from data import data

fake = Faker()

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session= sessionmaker(bind=engine)
    session = Session()
    
    sql = """
        DELETE FROM dev_event;
        DELETE FROM company_event;
    """
    session.execute('DELETE FROM dev_event;')
    session.execute('DELETE FROM company_event;')
    session.commit()
    
    session.query(Company).delete()
    session.query(Event).delete()
    session.query(Dev).delete()
    session.query(Freebie).delete()
    session.commit()
    
    companies  = [Company(name=fake.company(),  founding_year=random.randint(1980, 2025), industry=random.choice(data["tech_industries"])) for _ in range(30)]
    session.add_all(companies)
    session.commit()
    
    devs = [Dev(name= fake.name(), age = random.randint(18,60), email=fake.email(), role=random.choice(data["tech_roles"])) for _ in range(100)]
    session.add_all(devs)
    session.commit()
    
    events = []
    
    for name in data["tech_events"]:
        event = Event(
            name = name,
            organiser = fake.company(), 
            location = ', '.join(fake.location_on_land()[-1].split('/')),
            theme = fake.catch_phrase(),
            date_held = fake.date_time_this_decade()
        )
        
        event.devs = random.sample(devs, random.randint(30, 75))
        event.companies = random.sample(companies, random.randint(1, 5))
        # event.add_devs(event_devs, session)
            
        events.append(event)
    session.add_all(events)
    session.commit()
    
    freebies = []
    for company in companies:
        for i in range(random.randint(5, 20)):
            freebie_name = random.choice(data['freebies'])
            freebie = Freebie(
                name=freebie_name, 
                received_at= datetime.now(), 
                value= random.randint(5,30), 
                description=fake.text(max_nb_chars=100),
                company_id = company.id,
                dev_id = random.choice(devs).id)
            freebies.append(freebie)
            
    session.add_all(freebies)
    session.commit()
    
    # session.query(Company).delete()
    # session.query(Event).delete()
    # session.query(Dev).delete()
    # session.query(Freebie).delete()
    # session.commit()
        