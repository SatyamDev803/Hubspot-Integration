# hubspot.py

import asyncio
import base64
import json
import secrets
import httpx
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse
import urllib.parse
from integrations.integration_item import IntegrationItem
from redis_client import add_key_value_redis, delete_key_redis, get_value_redis

CLIENT_ID = '186e9160-76fd-4466-880c-a470f7923395'
CLIENT_SECRET = 'a10f2539-2269-4dfe-a530-f7c146bdd07a'
REDIRECT_URI = 'http://localhost:8000/integrations/hubspot/oauth2callback'
scope = 'oauth crm.objects.contacts.read'
authorization_url = 'https://app-na2.hubspot.com/oauth/authorize'


async def authorize_hubspot(user_id, org_id):
    state_data = {
        'state': secrets.token_urlsafe(32),
        'user_id': user_id,
        'org_id': org_id
    }

    encoded_state = base64.urlsafe_b64encode(json.dumps(state_data).encode('utf-8')).decode('utf-8')

    encoded_scope = urllib.parse.quote_plus(scope)

    auth_url = (
        f'{authorization_url}?client_id={CLIENT_ID}'
        f'&redirect_uri={REDIRECT_URI}'
        f'&scope={encoded_scope}'
        f'&state={encoded_state}'
    )

    await add_key_value_redis(f'hubspot_state:{org_id}:{user_id}', json.dumps(state_data), expire=600)

    return auth_url


async def oauth2callback_hubspot(request: Request):
    if request.query_params.get('error'):
        raise HTTPException(status_code=400, detail=request.query_params.get('error_description'))

    code = request.query_params.get('code')
    encoded_state = request.query_params.get('state')
    state_data = json.loads(base64.urlsafe_b64decode(encoded_state).decode('utf-8'))

    original_state = state_data.get('state')
    user_id = state_data.get('user_id')
    org_id = state_data.get('org_id')

    saved_state = await get_value_redis(f'hubspot_state:{org_id}:{user_id}')

    if not saved_state or original_state != json.loads(saved_state).get('state'):
        raise HTTPException(status_code=400, detail='State does not match.')

    async with httpx.AsyncClient() as client:
        response, _ = await asyncio.gather(
            client.post(
                'https://api.hubapi.com/oauth/v1/token',
                data={
                    'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': REDIRECT_URI,
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                },
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
            ),
            delete_key_redis(f'hubspot_state:{org_id}:{user_id}'),
        )
    
    await add_key_value_redis(f'hubspot_credentials:{org_id}:{user_id}', json.dumps(response.json()), expire=600)

    close_window_script = """
    <html>
        <script>
            window.close();
        </script>
    </html>
    """
    return HTMLResponse(content=close_window_script)


async def get_hubspot_credentials(user_id, org_id):
    credentials = await get_value_redis(f'hubspot_credentials:{org_id}:{user_id}')
    if not credentials:
        raise HTTPException(status_code=400, detail='No credentials found.')
    credentials = json.loads(credentials)
    if not credentials:
        raise HTTPException(status_code=400, detail='No credentials found.')
    # await delete_key_redis(f'hubspot_credentials:{org_id}:{user_id}')
    return credentials

def create_integration_item_metadata_object(response_json: dict) -> IntegrationItem:
    contact_id = response_json.get('id')
    properties = response_json.get('properties', {})

    firstname = properties.get('firstname', '')
    lastname = properties.get('lastname', '')
    name = f'{firstname} {lastname}'.strip() if firstname or lastname else f'Contact {contact_id}'

    creation_time = properties.get('createdate')
    last_modified_time = properties.get('lastmodifieddate')

    integration_item_metadata = IntegrationItem(
        id = contact_id,
        name = name,
        type='Contact',
        creation_time=creation_time,
        last_modified_time = last_modified_time
    )

    return integration_item_metadata
    

async def get_items_hubspot(user_id, org_id) -> list[IntegrationItem]:
    try:
        credentials = await get_hubspot_credentials(user_id, org_id)
        access_token = credentials.get('access_token')
    except HTTPException as e:
        print(f"Error retrieving credentials: {e.detail}")
        raise e
    
    url = "https://api.hubapi.com/crm/v3/objects/contacts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers = headers)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            print(f"HubSpot API error: {e.response_text}")
            raise HTTPException(status_code = e.response.status.code, detail = f"HubSpot API error: {e.response.text}")
        
    results = response.json().get('results', [])
    list_of_integration_items = []

    for item in results:
        list_of_integration_items.append(create_integration_item_metadata_object(item))

    print(f"list_of_integration_items: {list_of_integration_items}")

    return list_of_integration_items
    
