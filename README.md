# AI Automation Platform Suite

A comprehensive AI-powered automation platform that enables users to create, manage, and execute complex workflows using multiple AI agents. The platform provides a modern web interface for managing AI-driven automation tasks with real-time monitoring and analytics.

## 🚀 Features

### Core Capabilities
- **Multi-AI Provider Support**: Integration with OpenAI GPT-4 and Anthropic Claude models
- **Workflow Automation**: Visual workflow builder with drag-and-drop interface
- **AI Agent Management**: Create and configure specialized AI agents for different tasks
- **Real-time Monitoring**: Live dashboard with task execution tracking
- **Advanced Analytics**: Comprehensive reporting and performance metrics
- **Scheduled Execution**: Automated workflow triggers based on time, events, or webhooks
- **User Management**: Multi-user support with role-based access control

### AI Agent Types
- **Data Analysis Agents**: Specialized in processing and analyzing datasets
- **Content Generation Agents**: Expert in creating written content and copy
- **Email Automation Agents**: Handle personalized email campaigns
- **Web Scraping Agents**: Extract and process web data
- **API Integration Agents**: Connect with external services and APIs

### Workflow Templates
- **Data Analysis Workflow**: Automated data processing and reporting
- **Content Generation Workflow**: AI-powered content creation pipeline
- **Email Marketing Automation**: Personalized email campaign management
- **Custom Workflows**: Build your own automation sequences

## 🏗️ Architecture

### Backend (FastAPI)
- **API Server**: RESTful API with automatic documentation
- **AI Manager**: Centralized AI provider management and agent orchestration
- **Workflow Engine**: Task execution engine with scheduling capabilities
- **Database Layer**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT-based user authentication and authorization
- **Background Tasks**: Celery with Redis for async task processing

### Frontend (React + TypeScript)
- **Modern UI**: Material-UI components with responsive design
- **Real-time Updates**: WebSocket connections for live data
- **Interactive Charts**: Recharts for analytics visualization
- **State Management**: React Query for server state management
- **Routing**: React Router for single-page application navigation

### Infrastructure
- **Database**: PostgreSQL for persistent storage
- **Cache**: Redis for session management and task queuing
- **Task Queue**: Celery for background job processing
- **Monitoring**: Built-in analytics and system health monitoring

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Redis 6+
- OpenAI API Key (optional)
- Anthropic API Key (optional)

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ai-automation-platform
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

### 3. Database Setup
```bash
# Create PostgreSQL database
createdb ai_automation_db

# Run migrations (if using Alembic)
alembic upgrade head
```

### 4. Frontend Setup
```bash
# Install Node.js dependencies
npm install

# Set up environment variables
echo "REACT_APP_API_URL=http://localhost:8000" > .env.local
```

### 5. Redis Setup
```bash
# Start Redis server
redis-server

# Or using Docker
docker run -d -p 6379:6379 redis:alpine
```

## 🚀 Running the Application

### Development Mode

#### Start Backend Server
```bash
# Activate virtual environment
source venv/bin/activate

# Start FastAPI server
python backend/main.py
# Or using uvicorn directly
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

#### Start Celery Worker (Optional)
```bash
# In a separate terminal
celery -A backend.celery_app worker --loglevel=info
```

#### Start Frontend Development Server
```bash
# In a separate terminal
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Production Deployment

#### Using Docker (Recommended)
```bash
# Build and run with Docker Compose
docker-compose up -d
```

#### Manual Deployment
```bash
# Build frontend
npm run build

# Serve frontend with nginx or serve static files through FastAPI
# Configure reverse proxy to backend API
```

## 🔑 Environment Variables

### Backend (.env)
```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/ai_automation_db

# Redis
REDIS_URL=redis://localhost:6379

# AI API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# JWT Secret
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Settings
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Celery
CELERY_BROKER_URL=redis://localhost:6379
CELERY_RESULT_BACKEND=redis://localhost:6379
```

### Frontend (.env.local)
```env
REACT_APP_API_URL=http://localhost:8000
```

## 📚 API Documentation

The API documentation is automatically generated and available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints

#### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user info

#### Workflows
- `GET /api/workflows/` - List user workflows
- `POST /api/workflows/` - Create new workflow
- `PUT /api/workflows/{id}` - Update workflow
- `POST /api/workflows/{id}/execute` - Execute workflow
- `GET /api/workflows/templates/` - Get workflow templates

#### AI Agents
- `GET /api/agents/` - List available agents
- `POST /api/agents/` - Create new agent
- `POST /api/agents/{id}/execute` - Execute task with agent
- `GET /api/agents/types/` - Get agent types and configurations

#### Tasks
- `GET /api/tasks/` - List user tasks
- `GET /api/tasks/{id}` - Get task details
- `GET /api/tasks/stats/summary` - Get task statistics

#### Analytics
- `GET /api/analytics/dashboard` - Dashboard analytics
- `GET /api/analytics/tasks/timeline` - Task timeline data
- `GET /api/analytics/workflows/performance` - Workflow performance metrics

## 🎯 Usage Examples

### Creating a Data Analysis Workflow
```python
# Example workflow configuration
workflow_config = {
    "name": "Sales Data Analysis",
    "description": "Analyze monthly sales data and generate insights",
    "tasks": [
        {
            "name": "Load Data",
            "type": "data_processing",
            "config": {"source": "file", "format": "csv"}
        },
        {
            "name": "Analyze Data",
            "type": "ai_task",
            "agent": {"type": "openai", "tools": ["data_analysis"]},
            "prompt": "Analyze the sales data and identify key trends and insights"
        },
        {
            "name": "Generate Report",
            "type": "ai_task",
            "agent": {"type": "openai", "tools": ["file_processor"]},
            "prompt": "Create a comprehensive sales report with visualizations"
        }
    ],
    "triggers": [
        {
            "type": "schedule",
            "config": {"interval": "daily", "time": "09:00"}
        }
    ]
}
```

### Creating a Custom AI Agent
```python
# Example agent configuration
agent_config = {
    "name": "Customer Support Bot",
    "type": "openai",
    "description": "Handles customer inquiries and support tickets",
    "config": {
        "model": "gpt-4-turbo-preview",
        "temperature": 0.7,
        "max_tokens": 1000,
        "tools": ["web_search", "email_sender"]
    }
}
```

## 🔧 Development

### Project Structure
```
ai-automation-platform/
├── backend/                 # FastAPI backend
│   ├── core/               # Core functionality
│   │   ├── ai_manager.py   # AI provider management
│   │   └── workflow_engine.py # Workflow execution
│   ├── routers/            # API routes
│   │   ├── auth.py         # Authentication
│   │   ├── workflows.py    # Workflow management
│   │   ├── agents.py       # Agent management
│   │   ├── tasks.py        # Task management
│   │   └── analytics.py    # Analytics endpoints
│   ├── database.py         # Database models
│   └── main.py            # Application entry point
├── src/                    # React frontend
│   ├── components/         # Reusable components
│   ├── pages/             # Page components
│   ├── contexts/          # React contexts
│   └── App.tsx            # Main application
├── requirements.txt        # Python dependencies
├── package.json           # Node.js dependencies
└── README.md              # This file
```

### Adding New AI Providers
1. Extend the `AIManager` class in `backend/core/ai_manager.py`
2. Add provider-specific configuration in agent types
3. Update the frontend agent creation form

### Creating Custom Workflow Tasks
1. Add new task type in `WorkflowEngine._execute_task()`
2. Implement task-specific logic
3. Update workflow templates if needed

## 🧪 Testing

### Backend Tests
```bash
# Run backend tests
pytest backend/tests/
```

### Frontend Tests
```bash
# Run frontend tests
npm test
```

## 📊 Monitoring and Analytics

The platform includes comprehensive monitoring capabilities:

- **Real-time Dashboard**: Live metrics and system status
- **Task Analytics**: Execution history and performance trends
- **Agent Performance**: Success rates and usage statistics
- **System Health**: Uptime, response times, and error rates
- **Workflow Analytics**: Execution patterns and optimization insights

## 🔒 Security

- JWT-based authentication with configurable expiration
- Password hashing using bcrypt
- Role-based access control
- API rate limiting (configurable)
- Input validation and sanitization
- CORS protection

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the API documentation at `/docs`
- Review the examples in this README

## 🗺️ Roadmap

- [ ] Visual workflow builder with drag-and-drop interface
- [ ] More AI provider integrations (Google PaLM, Azure OpenAI)
- [ ] Advanced scheduling with cron expressions
- [ ] Workflow version control and rollback
- [ ] Plugin system for custom integrations
- [ ] Mobile application
- [ ] Advanced user roles and permissions
- [ ] Audit logging and compliance features
- [ ] Multi-tenant support
- [ ] API marketplace for sharing workflows

---

Built with ❤️ using FastAPI, React, and the power of AI automation.