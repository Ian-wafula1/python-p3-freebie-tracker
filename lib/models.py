from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, DateTime, Table, func
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

dev_event = Table(
    'dev_event',
    Base.metadata,
    Column('dev_id', Integer, ForeignKey('devs.id', ondelete='CASCADE'), primary_key=True),
    Column('event_id', Integer, ForeignKey('events.id', ondelete='CASCADE'), primary_key=True),
    extend_existing=True
)

company_event = Table(
    'company_event',
    Base.metadata,
    Column('company_id', Integer, ForeignKey('companies.id', ondelete='CASCADE'), primary_key=True),
    Column('event_id', Integer, ForeignKey('events.id', ondelete='CASCADE'), primary_key=True),
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
    devs = association_proxy('freebies', 'dev', creator = lambda dv: Freebie(dev=dv))
    
    @classmethod
    def oldest_company(cls, session):
        oldest = session.query(cls).order_by(cls.founding_year).first()
        return oldest if oldest else None
    
    def give_freebie(self, dev, item_name, value, session):
        freebie = Freebie(name=item_name, value=value, company_id = self.id, dev_id=dev.id)
        session.add(freebie)
        session.commit()
        return freebie
        
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
    companies = association_proxy('freebies', 'company', creator = lambda co: Freebie(company = co))
    
    def received_one(self, item_name, session):
        return bool(session.query(Freebie).filter_by(name=item_name))
    
    def give_away(self,dev, freebie, session):
        if freebie in self.freebies:
            freebie.dev_id = dev.id
            session.commit()
            return 'Freebie given away successfully'
        return 'Freebie not found in this developer\'s freebies'

    def __repr__(self):
        return f'<Dev {self.id}: {self.name}>, {self.role}'

class Freebie(Base):
    __tablename__ = 'freebies'
    
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    value = Column(Integer())
    description = Column(String())
    received_at = Column(DateTime(), server_default=func.now())
    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    
    company = relationship('Company', back_populates='freebies')
    dev = relationship('Dev', back_populates='freebies')
    
    def print_details(self):
        return f"{self.dev} owns a {self.name} from {self.company}"
    
    def __repr__(self):
        return f"<Freebie {self.id}: {self.name}, Value: ${self.value}>"

class Event(Base):
    __tablename__ = 'events'
    
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    organiser = Column(String())
    theme = Column(String())
    location = Column(String())
    date_held = Column(DateTime(), server_default=func.now())
    
    companies = relationship('Company', back_populates='events', secondary=company_event)
    devs = relationship('Dev', back_populates='events', secondary=dev_event)
    
    # Returns the freebies given at the event
    
    def freebies(self, session):
        return session.query(Freebie).filter(Freebie.company.has(Company.events.any(id=self.id))).all()
    
    def add_devs(self, devs, session):
        for dev in devs:
            if dev not in self.devs:
                self.devs.append(dev)
            session.commit() 
        # self.devs.extend(devs)
        # session.commit()   
                
    def __repr__(self):
        return f"<Event {self.id}: {self.name}>"
    
    # aggregate methods
