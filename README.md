## Hubspot Integration

The project includes a comprehensive Hubspot CRM integration that allows:

- OAuth2 Authentication with Hubspot
- Contact Management (CRM.objects.contacts access)
- Secure credential management using Redis
- User and organization-specific configurations

### Hubspot Configuration

1. Hubspot API Setup:
   - Client ID: 'Your Client ID'
   - Redirect URI: `http://localhost:8000/integrations/hubspot/oauth2callback`
   - Required Scopes: `oauth crm.objects.contacts.read`

2. Backend Endpoints:
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

## Development

The project uses:
- FastAPI for the backend API
- React for the frontend interface
- Redis for caching
- OAuth2 for authentication


