# 🧢 Dev Freebie Tracker

Track and manage all the awesome tech swag (aka freebies) developers collect at hackathons, meetups, and conferences. This app lets you manage devs, companies, events, and the goodies handed out along the way.

## 📦 Features

- Track developers and their roles
- Store company details
- Add and manage tech events
- Record freebies handed out to devs by companies
- Many-to-many relationships between Devs, Events and Companies
- Keeps track of the devs and companies that attended an event
- Keeps track of all the freebies handed out at an event 

## 🧱 Tech Stack

- Python 3.11+
- SQLAlchemy ORM
- SQLite3
- Alembic for migrations
- Spotify (for REAL vibe coding 😎🎵)

## 🧮 Models

### `Dev`
- Holds data for developers 
- **Relationships**:
  - `freebies`: One-to-Many
  - `events`: Many-to-Many via `dev_event`

### `Company`
- Data for companies that participated in events
- **Relationships**:
  - `freebies`: One-to-Many
  - `events`: Many-to-Many via `company_event`

### `Event`
- Data for different events
- **Relationships**:
  - `devs`: Many-to-Many via `dev_event`
  - `companies`: Many-to-Many via `company_event`
  - `freebies`: One-to-Many (indirectly through `devs` or `companies`)

### `Freebie`
- Freebies handed out by companies in events
- **Relationships**
  - `devs`: One-to-Many
  - `companies`: One-to-Many
  - `events`: One-to-Many (indirectly through `devs` or `companies`)

## 🧪 Setup Instructions

1. Clone the repo and navigate into the folder

```bash
git clone https://github.com/your-username/dev-freebie-tracker.git
cd dev-freebie-tracker
```
2. Launch the virtual environment for the project
```bash
pipenv install && pipenv shell
```

3. Run migrations
```bash
alembic upgrade head
```

4. Generate seed data
```bash
cd lib
python seed.py
```

5. Run the debug file to interact with the system
```bash
python debug.py
```

## 🧾 License

- MIT — use, remix, build on it freely.