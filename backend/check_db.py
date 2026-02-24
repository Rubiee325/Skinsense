import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

async def check_users():
    load_dotenv()
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    database_name = os.getenv("MONGODB_DATABASE", "skinmorph")
    
    print("=" * 60)
    print("Database Content Check")
    print("=" * 60)
    
    client = AsyncIOMotorClient(mongodb_url)
    db = client[database_name]
    
    try:
        # Check users
        users_count = await db.users.count_documents({})
        print(f"Total Users: {users_count}")
        
        if users_count > 0:
            print("\nLatest Users:")
            async for user in db.users.find().sort("created_at", -1).limit(5):
                print(f"- Name: {user.get('name')}")
                print(f"  Email: {user.get('email')}")
                print(f"  Role: {user.get('role')}")
                print(f"  Created: {user.get('created_at')}")
                print("-" * 30)
        
        # Check predictions
        pred_count = await db.predictions.count_documents({})
        print(f"\nTotal Predictions/Reports: {pred_count}")
        
    except Exception as e:
        print(f"Error checking database: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(check_users())
