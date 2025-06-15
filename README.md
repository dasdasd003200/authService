# AuthService - Scalable Authentication Microservice

A Django-based authentication microservice with GraphQL API, built for scalability and security.

## Features

- **Custom User Model** extending Django's AbstractUser
- **GraphQL API** for all authentication operations
- **JWT Authentication** with refresh tokens
- **Email Verification** and password reset
- **Account Security** (lockout after failed attempts)
- **Session Management** with tracking
- **PostgreSQL** database with optimized queries
- **Redis** caching for performance
- **Docker** containerization
- **Security Middleware** and headers
- **Rate Limiting** protection
- **Comprehensive Logging** and monitoring

## Tech Stack

- **Django 5.2** - Web framework
- **GraphQL** (graphene-django) - API layer
- **PostgreSQL** - Primary database
- **Redis** - Caching and sessions
- **JWT** - Token authentication
- **Docker** - Containerization
- **Nginx** - Reverse proxy (production)

## Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd authservice
cp .env.example .env
# Edit .env with your configuration
```

### 2. Using Docker (Recommended)

```bash
docker-compose -f docker/docker-compose.yml up -d
```

### 3. Manual Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/development.txt

# Setup database
python manage.py migrate
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## GraphQL API

The API is available at `/graphql/` with GraphiQL interface enabled in development.

### Authentication Flow

#### 1. Register User

```graphql
mutation {
  registerUser(
    username: "testuser"
    email: "test@example.com"
    password: "SecurePass123!"
    firstName: "Test"
    lastName: "User"
  ) {
    success
    errors
    message
    user {
      id
      email
      username
    }
  }
}
```

#### 2. Verify Email

```graphql
mutation {
  verifyEmail(token: "your-verification-token") {
    success
    errors
    message
    user {
      id
      isEmailVerified
    }
  }
}
```

#### 3. Login (Get JWT Token)

```graphql
mutation {
  tokenAuth(email: "test@example.com", password: "SecurePass123!") {
    token
    refreshToken
    user {
      id
      email
      username
    }
  }
}
```

#### 4. Get Current User

```graphql
query {
  me {
    id
    email
    username
    fullName
    status
    isEmailVerified
  }
}
```

### User Management

#### Update Profile

```graphql
mutation {
  updateProfile(
    firstName: "Updated"
    lastName: "Name"
    timezone: "America/New_York"
  ) {
    success
    errors
    user {
      id
      fullName
      timezone
    }
  }
}
```

#### Change Password

```graphql
mutation {
  changePassword(currentPassword: "OldPass123!", newPassword: "NewPass123!") {
    success
    errors
  }
}
```

### Password Reset

#### Request Reset

```graphql
mutation {
  requestPasswordReset(email: "test@example.com") {
    success
    message
  }
}
```

#### Reset Password

```graphql
mutation {
  resetPassword(token: "reset-token", newPassword: "NewPass123!") {
    success
    errors
    message
  }
}
```

### Session Management

#### Get Active Sessions

```graphql
query {
  activeSessions {
    id
    ipAddress
    userAgent
    lastActivity
    isExpired
  }
}
```

#### Logout Current Session

```graphql
mutation {
  logoutUser {
    success
    message
  }
}
```

#### Invalidate All Sessions

```graphql
mutation {
  invalidateAllSessions {
    success
    message
  }
}
```

## Project Structure

```
authservice/
├── authservice/           # Main project configuration
│   ├── settings/         # Environment-specific settings
│   ├── schema.py         # Main GraphQL schema
│   └── urls.py           # URL configuration
├── apps/                 # Application modules
│   ├── core/            # Core utilities and base models
│   ├── users/           # User management
│   └── authentication/ # Authentication logic
├── docker/              # Docker configuration
├── requirements/        # Python dependencies
├── tests/              # Test files
└── docs/               # Documentation
```

## Configuration

### Environment Variables

Key environment variables (see `.env.example`):

- `SECRET_KEY` - Django secret key
- `DB_NAME`, `DB_USER`, `DB_PASSWORD` - Database configuration
- `REDIS_URL` - Redis connection string
- `EMAIL_*` - Email configuration
- `FRONTEND_URL` - Frontend application URL
- `SENTRY_DSN` - Error tracking (optional)

### Settings Files

- `base.py` - Common settings
- `development.py` - Development environment
- `production.py` - Production environment
- `testing.py` - Test environment

## Security Features

### Account Protection

- Account lockout after 5 failed login attempts
- Password strength validation
- Session tracking and management
- Rate limiting on API endpoints

### Security Headers

- XSS Protection
- Content Type Options
- Frame Options
- Referrer Policy
- Permissions Policy

### Data Protection

- JWT token expiration
- Secure cookie settings
- CORS configuration
- CSRF protection

## Database Models

### User Model

Extended Django AbstractUser with additional fields:

- Email verification status
- Phone number
- Account status
- Security tracking fields
- Profile information

### Session Tracking

- IP address and user agent logging
- Session expiration management
- Multi-device session support

### Token Management

- Email verification tokens
- Password reset tokens
- Automatic cleanup of expired tokens

## Deployment

### Production Checklist

1. **Environment Configuration**

   ```bash
   export DJANGO_SETTINGS_MODULE=authservice.settings.production
   ```

2. **Database Setup**

   ```bash
   python manage.py migrate
   python manage.py collectstatic
   ```

3. **Security Settings**

   - Set `DEBUG=False`
   - Configure `ALLOWED_HOSTS`
   - Set secure cookie flags
   - Configure HTTPS redirects

4. **Monitoring**
   - Configure Sentry for error tracking
   - Set up log aggregation
   - Monitor database performance

### Docker Production

```bash
docker-compose -f docker/docker-compose.prod.yml up -d
```

## Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.users
python manage.py test apps.authentication

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## API Documentation

### GraphQL Schema

The complete schema is available at `/graphql/` in development mode with GraphiQL interface.

### Authentication Headers

Include JWT token in requests:

```
Authorization: Bearer <your-jwt-token>
```

## Monitoring and Logging

### Log Files

- `logs/django.log` - Application logs
- `logs/error.log` - Error logs (production)

### Health Check

- Endpoint: `/health/`
- Returns service status and database connectivity

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## Best Practices

### Security

- Always use HTTPS in production
- Regularly rotate secret keys
- Monitor failed login attempts
- Keep dependencies updated

### Performance

- Use database indexes effectively
- Implement caching strategies
- Monitor query performance
- Use connection pooling

### Scalability

- Design stateless services
- Use Redis for session storage
- Implement proper logging
- Monitor resource usage

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:

- Create an issue in the repository
- Check the documentation in `/docs/`
- Review the GraphQL schema at `/graphql/`

