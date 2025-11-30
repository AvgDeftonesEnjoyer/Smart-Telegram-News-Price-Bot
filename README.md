# 🤖 Smart Telegram News & Price Bot

A Django-based Telegram bot for tracking cryptocurrency news and prices with topic subscription functionality.

## 📋 Table of Contents

- [Features](#-features)
- [Technologies](#-technologies)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Bot Commands](#-bot-commands)
- [API Endpoints](#-api-endpoints)
- [Development](#-development)
- [Project Structure](#-project-structure)

## ✨ Features

- 🔔 **Topic Subscriptions**: Users can subscribe to different topics (crypto, stocks, news)
- 💰 **Cryptocurrency**: Get trending cryptocurrencies from CoinGecko API
- 🗄️ **Database**: PostgreSQL for storing users and subscriptions
- ⚡ **Caching**: Redis for optimizing external API requests
- 🌐 **REST API**: Django REST Framework for web integrations
- 🐳 **Docker**: Full containerization for easy deployment
- 🎛️ **Django Admin**: Web interface for data management

## 🛠️ Technologies

- **Backend**: Django 5.2.8, Django REST Framework 3.15.2
- **Bot Framework**: python-telegram-bot 21.10
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Containerization**: Docker, Docker Compose
- **Language**: Python 3.11

## 🏗️ Architecture

The project consists of four main services:

1. **Bot Service** (`smartbot_app`) - Telegram bot for user interaction
2. **Backend Service** (`smartbot_backend`) - Django web server (Admin + API) on port 8000
3. **Database Service** (`smartbot_db`) - PostgreSQL database
4. **Cache Service** (`smartbot_redis`) - Redis for caching

```
┌─────────────────┐      ┌─────────────────┐
│  Telegram Bot   │      │  Django Backend │
│  (Port: N/A)    │      │  (Port: 8000)   │
└────────┬────────┘      └────────┬────────┘
         │                        │
         └────────┬───────────────┘
                  │
         ┌────────▼────────┐
         │   PostgreSQL    │
         │   (Port: 5432)  │
         └─────────────────┘
                  │
         ┌────────▼────────┐
         │      Redis      │
         │   (Port: 6379)  │
         └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Telegram Bot Token (get from [@BotFather](https://t.me/botfather))

### Step 1: Clone the repository

```bash
git clone <repository-url>
cd Smart-Telegram-News-Price-Bot
```

### Step 2: Configure environment variables

Create a `.env` file in the root directory:

```env
# Telegram Bot
BOT_TOKEN=your_telegram_bot_token_here

# CoinGecko API
COINGECKO_TRENDING_URL=https://api.coingecko.com/api/v3/search/trending

# Database (already configured in docker-compose.yml)
DB_HOST=db
DB_NAME=smartbot_db
DB_USER=postgres
DB_PASSWORD=password
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
```

### Step 3: Start the project

```bash
cd Docker
docker compose up --build
```

This will start all services:

- ✅ PostgreSQL database
- ✅ Redis cache
- ✅ Telegram bot
- ✅ Django web server

### Step 4: Create a superuser (for Admin access)

```bash
docker compose exec backend python manage.py createsuperuser
```

### Step 5: Access the services

- **Django Admin**: http://localhost:8000/admin/
- **API**: http://localhost:8000/api/
- **Telegram Bot**: Find your bot in Telegram and send `/start`

## 🤖 Bot Commands

| Command                | Description                   | Example               |
| ---------------------- | ----------------------------- | --------------------- |
| `/start`               | Register/greet user           | `/start`              |
| `/subscribe [topic]`   | Subscribe to a topic          | `/subscribe crypto`   |
| `/unsubscribe [topic]` | Unsubscribe from a topic      | `/unsubscribe crypto` |
| `/crypto`              | Get trending cryptocurrencies | `/crypto`             |

### Available topics:

- `crypto` - Cryptocurrencies
- `stocks` - Stocks
- `news` - News

## 🌐 API Endpoints

### Topics

```http
GET /api/topics/
```

Get a list of all available topics.

### Subscriptions

```http
GET /api/subscriptions/
```

Get current user's subscriptions.

```http
POST /api/subscribe/
Content-Type: application/json

{
  "topic_id": 1
}
```

Subscribe to a topic.

```http
POST /api/unsubscribe/
Content-Type: application/json

{
  "topic_id": 1
}
```

Unsubscribe from a topic.

### Feed

```http
GET /api/topics/{topic_id}/feed/
```

Get news feed for a specific topic.

## 💻 Development

### Running Django commands

All Django commands must be executed inside the Docker container:

```bash
# Migrations
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate

# Django shell
docker compose exec backend python manage.py shell

# Create app
docker compose exec backend python manage.py startapp app_name

# Collect static files
docker compose exec backend python manage.py collectstatic
```

### View logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f bot
docker compose logs -f backend
docker compose logs -f db
docker compose logs -f redis
```

### Stop services

```bash
# Stop all containers
docker compose down

# Stop and remove volumes (WARNING: will delete DB data!)
docker compose down -v
```

### Restart specific service

```bash
docker compose restart bot
docker compose restart backend
```

## 📁 Project Structure

```
Smart-Telegram-News-Price-Bot/
├── backend/                      # Django backend
│   ├── bot/                      # Telegram bot logic
│   │   ├── main.py              # Bot entry point
│   │   ├── handlers.py          # Command handlers
│   │   └── default_topics.py    # Topic list
│   ├── news_providers/          # News providers
│   │   ├── crypto.py            # CoinGecko integration
│   │   └── redis_client.py      # Redis client
│   ├── users/                   # Users app
│   │   ├── models.py            # CustomUser model
│   │   └── admin.py             # Admin configuration
│   ├── subscriptions/           # Subscriptions app
│   │   ├── models.py            # Subscription model
│   │   └── admin.py             # Admin configuration
│   ├── topics/                  # Topics app
│   │   ├── models.py            # Topic, FeedItem models
│   │   ├── views.py             # API views
│   │   ├── serializers.py       # DRF serializers
│   │   ├── urls.py              # URL routing
│   │   └── admin.py             # Admin configuration
│   ├── smart_bot/               # Django project
│   │   ├── settings.py          # Settings
│   │   └── urls.py              # Main URL config
│   ├── requirements.txt         # Python dependencies
│   └── manage.py                # Django CLI
├── Docker/
│   ├── docker-compose.yml       # Service orchestration
│   └── Dockerfile               # Docker image
├── .env                         # Environment variables (gitignored)
├── .gitignore
└── README.md
```

## 🗄️ Database Models

### CustomUser

```python
- telegram_id: CharField (unique)
- username: CharField (unique)
- + standard Django AbstractUser fields
```

### Topic

```python
- name: CharField (unique)
- created_at: DateTimeField
- updated_at: DateTimeField
```

### Subscription

```python
- user: ForeignKey(CustomUser)
- topic: ForeignKey(Topic)
- created_at: DateTimeField
- unique_together: (user, topic)
```

### FeedItem

```python
- topic: ForeignKey(Topic)
- title: CharField
- url: URLField
- source: CharField
- created_at: DateTimeField
```

## 🔧 Configuration

### Django Settings

Main settings in `backend/smart_bot/settings.py`:

```python
# Telegram Bot
BOT_TOKEN = os.getenv('BOT_TOKEN')

# CoinGecko API
COINGECKO_TRENDING_URL = os.getenv('COINGECKO_TRENDING_URL')

# Redis
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))

# Custom User Model
AUTH_USER_MODEL = 'users.CustomUser'
```

## 🐛 Troubleshooting

### Bot not starting

1. Check if `BOT_TOKEN` is correctly set in `.env`
2. View logs: `docker compose logs -f bot`

### Database unavailable

1. Check if PostgreSQL container is running: `docker compose ps`
2. Check healthcheck: `docker compose exec db pg_isready -U postgres`

### Migration errors

```bash
# Check migration status
docker compose exec backend python manage.py showmigrations

# Apply migrations
docker compose exec backend python manage.py migrate
```

## 📝 TODO / Future Improvements

- [ ] Add providers for stocks and news
- [ ] Implement periodic news broadcasting to subscribers
- [ ] Add Celery for background tasks
- [ ] Expand bot command functionality
- [ ] Add tests (pytest)
- [ ] Set up CI/CD
- [ ] Add Docker production configuration
- [ ] Improve error handling

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

Your Name / Team

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
