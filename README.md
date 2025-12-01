# FairFound Extension Backend

Django REST Framework backend powering the FairFound Chrome Extension. Provides leaderboard rankings and freelancer comparison APIs.

## Features

- **100 Realistic Freelancers**: Seeded dummy data with varied metrics across performance tiers
- **15 Specialty Categories**: Full Stack, Frontend, Backend, Mobile, UI/UX, Data Science, DevOps, and more
- **Dual Ranking System**: Marketplace scores vs FairFound's proprietary scoring
- **Category Filtering**: Filter leaderboards by freelancer specialty
- **Comparison API**: Compare any two freelancers by profile URL
- **Comparison History**: Track all comparisons for analytics

## Tech Stack

- Python 3.10+
- Django 4.2
- Django REST Framework 3.14
- PostgreSQL
- django-cors-headers

## Quick Start

### 1. Create Virtual Environment
```bash
cd FairFound_Backend_Extension
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy example env file
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# Edit .env with your database credentials
```

### 4. Create PostgreSQL Database
```sql
CREATE DATABASE fairfound_extension;
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Seed Sample Data (100 Freelancers)
```bash
python manage.py seed_data
```

### 7. Start Development Server
```bash
python manage.py runserver
```

Server runs at `http://localhost:8000`

## API Endpoints

### Leaderboards

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/leaderboard/` | List all freelancers (paginated) |
| GET | `/api/leaderboard/categories/` | Get all specialty categories |
| GET | `/api/leaderboard/marketplace/` | Top 20 by marketplace score |
| GET | `/api/leaderboard/marketplace/?category=X` | Filtered by specialty |
| GET | `/api/leaderboard/fairfound/` | Top 20 by FairFound score |
| GET | `/api/leaderboard/fairfound/?category=X` | Filtered by specialty |
| GET | `/api/leaderboard/profiles/` | All profiles with URLs |
| GET | `/api/leaderboard/profiles/?search=X` | Search by name |

### Comparison

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/compare/` | Compare two freelancers |

#### Compare Request Body
```json
{
  "url1": "https://fairfound.com/freelancer/sarah-johnson",
  "url2": "https://fairfound.com/freelancer/michael-chen"
}
```

#### Compare Response
```json
{
  "freelancer1": { "name": "Sarah Johnson", "url": "..." },
  "freelancer2": { "name": "Michael Chen", "url": "..." },
  "metrics": [
    { "label": "Rating", "value1": 4.9, "value2": 4.8, "suffix": "" },
    { "label": "Jobs Done", "value1": 156, "value2": 203, "suffix": "" },
    { "label": "On-Time", "value1": 94, "value2": 96, "suffix": "%" },
    { "label": "Response", "value1": 2, "value2": 1, "suffix": "h" },
    { "label": "Rehire Rate", "value1": 78, "value2": 85, "suffix": "%" },
    { "label": "FairFound Score", "value1": 87, "value2": 92, "suffix": "" }
  ],
  "winner": "Michael Chen"
}
```

## Project Structure

```
FairFound_Backend_Extension/
├── config/                 # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── leaderboard/            # Freelancer & leaderboard app
│   ├── models.py           # Freelancer model
│   ├── views.py            # Leaderboard ViewSet
│   ├── serializers.py
│   ├── urls.py
│   ├── admin.py
│   └── management/
│       └── commands/
│           └── seed_data.py  # Generate 100 freelancers
├── comparisons/            # Comparison app
│   ├── models.py           # ComparisonHistory model
│   ├── views.py            # Compare API view
│   ├── serializers.py
│   └── urls.py
├── manage.py
├── requirements.txt
├── .env.example
└── api_endpoints.http      # API test file (VS Code REST Client)
```

## Data Model

### Freelancer
| Field | Type | Description |
|-------|------|-------------|
| name | CharField | Full name |
| profile_url | URLField | Unique profile URL |
| specialty | CharField | Job category |
| platform | CharField | Source platform |
| marketplace_rating | Decimal | Platform rating (0-5) |
| marketplace_score | Integer | Platform ranking score |
| fairfound_score | Integer | Calculated FairFound score |
| jobs_completed | Integer | Total jobs done |
| on_time_percentage | Integer | On-time delivery % |
| response_time_hours | Integer | Avg response time |
| rehire_rate | Integer | Client rehire % |

## FairFound Score Algorithm

The proprietary FairFound score considers multiple factors:

```python
score = (
    (rating * 10) +           # Rating weight
    (on_time * 0.3) +         # Reliability weight
    (min(jobs, 200) * 0.1) +  # Experience weight (capped)
    (rehire_rate * 0.2) +     # Client satisfaction weight
    ((24 - response_hours) * 0.5)  # Responsiveness weight
)
```

This creates a more balanced ranking than marketplace scores alone.

## Freelancer Categories

- Full Stack Developer
- Frontend Developer
- Backend Developer
- Mobile Developer
- UI/UX Designer
- Data Scientist
- DevOps Engineer
- Cloud Architect
- Machine Learning Engineer
- Blockchain Developer
- Game Developer
- WordPress Developer
- Shopify Developer
- React Developer
- Python Developer

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DEBUG | Debug mode | True |
| SECRET_KEY | Django secret key | (required) |
| DATABASE_NAME | PostgreSQL database | fairfound_extension |
| DATABASE_USER | Database user | postgres |
| DATABASE_PASSWORD | Database password | (required) |
| DATABASE_HOST | Database host | localhost |
| DATABASE_PORT | Database port | 5432 |
| ALLOWED_HOSTS | Allowed hosts | localhost,127.0.0.1 |
| CORS_ALLOWED_ORIGINS | CORS origins | http://localhost:3000 |

## Admin Panel

Access the Django admin at `http://localhost:8000/admin/`

Create a superuser:
```bash
python manage.py createsuperuser
```

## Testing API

Use the included `api_endpoints.http` file with VS Code REST Client extension, or use curl:

```bash
# Get categories
curl http://localhost:8000/api/leaderboard/categories/

# Get FairFound leaderboard
curl http://localhost:8000/api/leaderboard/fairfound/

# Compare freelancers
curl -X POST http://localhost:8000/api/compare/ \
  -H "Content-Type: application/json" \
  -d '{"url1":"https://fairfound.com/freelancer/sarah-johnson","url2":"https://fairfound.com/freelancer/michael-chen"}'
```

## License

Proprietary - FairFound Project
