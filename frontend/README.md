# Integrations Project

This project provides a unified interface for integrating with various third-party services including Hubspot, Airtable, and Notion. It consists of a React frontend and a FastAPI backend.

## Hubspot Integration

The project includes a comprehensive Hubspot CRM integration that allows:

- OAuth2 Authentication with Hubspot
- Contact Management (CRM.objects.contacts access)
- Secure credential management using Redis
- User and organization-specific configurations

### Hubspot Configuration

1. Hubspot API Setup:
   - Client ID: `186e9160-76fd-4466-880c-a470f7923395`
   - Redirect URI: `http://localhost:8000/integrations/hubspot/oauth2callback`
   - Required Scopes: `oauth crm.objects.contacts.read`

2. Frontend Features:
   - Material-UI based interface
   - Real-time connection status
   - Popup OAuth flow
   - Automatic credential management

3. Backend Endpoints:
   ```
   POST /integrations/hubspot/authorize
   - Purpose: Initiate OAuth flow
   - Parameters: user_id, org_id
   - Returns: Authorization URL

   GET /integrations/hubspot/oauth2callback
   - Purpose: Handle OAuth callback
   - Parameters: code, state
   - Returns: Authorization success/failure

   POST /integrations/hubspot/credentials
   - Purpose: Retrieve stored credentials
   - Parameters: user_id, org_id
   - Returns: Hubspot credentials

   POST /integrations/hubspot/load
   - Purpose: Load Hubspot data
   - Parameters: credentials
   - Returns: Hubspot items
   ```

## Project Structure

```
├── backend/
│   ├── main.py              # FastAPI main application
│   ├── redis_client.py      # Redis client for caching
│   ├── requirements.txt     # Python dependencies
│   └── integrations/        # Integration implementations
│       ├── airtable.py
│       ├── hubspot.py
│       └── notion.py
└── frontend/
    ├── src/
    │   ├── App.js          # Main React application
    │   ├── data-form.js    # Data form components
    │   └── integrations/   # Integration-specific components
    └── public/             # Static assets
```

## Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

The backend server will run on `http://localhost:8000`

## Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The React application will run on `http://localhost:3000`

## Features

### Hubspot Features
- Full OAuth2 authentication flow with secure state management
- Contact data retrieval and management
- Real-time connection status monitoring
- Automatic token refresh handling
- Secure credential storage in Redis
- Organization and user-level isolation
- Material-UI based integration interface

### General Features
- Multi-platform OAuth2 integration (Hubspot, Airtable, Notion)
- Data synchronization between platforms
- Redis caching for improved performance
- Cross-Origin Resource Sharing (CORS) enabled
- User and organization-based authentication
- Error handling and user feedback
- Secure credential management

## API Endpoints

### Airtable
- POST `/integrations/airtable/authorize` - Initiate OAuth flow
- GET `/integrations/airtable/oauth2callback` - OAuth callback
- POST `/integrations/airtable/credentials` - Get credentials
- POST `/integrations/airtable/load` - Load items

### Notion
- POST `/integrations/notion/authorize` - Initiate OAuth flow
- GET `/integrations/notion/oauth2callback` - OAuth callback

### Hubspot
- Similar endpoints for Hubspot integration

## Development

The project uses:
- FastAPI for the backend API
- React for the frontend interface
- Redis for caching
- OAuth2 for authentication

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

