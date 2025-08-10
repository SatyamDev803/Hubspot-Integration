import asyncio
from integrations import hubspot

async def get_auth_url():
    user_id = "TestUser"
    org_id = "TestOrg"
    auth_url = await hubspot.authorize_hubspot(user_id, org_id)
    print(f"Ppen this URL in browser: {auth_url}")

if __name__ == "__main__":
    asyncio.run(get_auth_url())