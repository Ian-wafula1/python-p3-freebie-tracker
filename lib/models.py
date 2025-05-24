from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, DateTime, Table, func
from datetime import datetime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

dev_event = Table(
    'dev_event',
    Base.metadata,
    Column('dev_id', Integer, ForeignKey('devs.id'), primary_key=True),
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True),
    extend_existing=True
)

company_event = Table(
    'company_event',
    Base.metadata,
    Column('company_id', Integer, ForeignKey('companies.id'), primary_key=True),
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True),
    extend_existing=True
)
class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())
    industry = Column(String())
    
    freebies = relationship('Freebie', back_populates='company', cascade='save-update, merge')
    events = relationship('Event', back_populates='companies', secondary=company_event)

    def __repr__(self):
        return f'<Company {self.id}: {self.name}>'

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())
    age = Column(Integer())
    email = Column(String())
    role = Column(String())
    
    freebies = relationship('Freebie', back_populates='dev', cascade='save-update, merge')
    events = relationship('Event', back_populates='devs', secondary=dev_event)

    def __repr__(self):
        return f'<Dev {self.id}: {self.name}>, {self.role}'

class Freebie(Base):
    __tablename__ = 'freebies'
    
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    category = Column(String())
    description = Column(String())
    received_at = Column(DateTime(), server_default=func.now())
    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    event_id = Column(Integer(), ForeignKey('events.id'))
    
    company = relationship('Company', back_populates='freebies')
    dev = relationship('Dev', back_populates='freebies')
    event = relationship('Event', back_populates='freebies')
    
    def __repr__(self):
        return f"<Freebie {self.id}: {self.name}, Category: {self.category}, Received at: {self.received_at}>"

class Event(Base):
    __tablename__ = 'events'
    
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    organiser = Column(String())
    theme = Column(String())
    location = Column(String())
    date_held = Column(DateTime(), server_default=func.now())
    
    freebies = relationship('Freebie', back_populates='event')
    companies = relationship('Company', back_populates='events', secondary=company_event)
    devs = relationship('Dev', back_populates='events', secondary=dev_event)
    
    def __repr__(self):
        return f"<Event {self.id}: {self.name}>"
