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
    
    # events = [Event(name=data["tech_events"][i], location=fake.location_on_land(), date_held=fake.date_time_this_decade()) for i in range(len(data["tech_events"]))]
    # session.add_all(events)
    # session.commit()
    
    events = [Event(name=name, organiser = fake.company(), location=', '.join(fake.location_on_land()[-1].split('/')), theme = fake.catch_phrase(), date_held=fake.date_time_this_decade()) for name in data["tech_events"]]
    # events = []
    # for event_name in data["tech_events"]:
    #     event = Event(name = event_name,
    #                   organiser = fake.company(),
    #                   theme = fake.catch_phrase(), 
    #                   location = fake.location_on_land(),
    #                   date_held = fake.date_time_this_decade()
    #     )
    #     events.append(event)
    
    session.add_all(events)
    session.commit()
    
    freebies = []
    for company in companies:
        for i in range(random.randint(5, 20)):
            freebie_name, category = random.choice(data['freebies'])
            freebie = Freebie(name=freebie_name, category=category, received_at= datetime.now(),  description=fake.text(max_nb_chars=100),company_id = company.id )
            freebies.append(freebie)
            
    session.add_all(freebies)
    session.commit()
        