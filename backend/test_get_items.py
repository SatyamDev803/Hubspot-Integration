import asyncio
from integrations import hubspot

async def test_get_hubspot_items():
    user_id = "TestUser"
    org_id = "TestOrg"
    print("Fetching items from HubSpot...")
    items = await hubspot.get_items_hubspot(user_id, org_id)
    print("Items fetched successfully.")
    for item in items:
        print(f"ID: {item.id}, Name: {item.name}, Type: {item.type}")

if __name__ == "__main__":
    asyncio.run(test_get_hubspot_items())