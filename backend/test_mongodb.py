"""
Quick script to test MongoDB connection.
Run this to verify your MongoDB setup is working.
"""
import asyncio
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("WARNING: python-dotenv not installed. Install with: pip install python-dotenv")
    print("   (You can still use environment variables directly)")

from motor.motor_asyncio import AsyncIOMotorClient


async def test_mongodb_connection():
    """Test MongoDB connection."""
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    database_name = os.getenv("MONGODB_DATABASE", "skinmorph")
    
    print(f"INFO: Testing MongoDB connection...")
    print(f"   URL: {mongodb_url.replace('://', '://***:***@') if '@' in mongodb_url else mongodb_url}")
    print(f"   Database: {database_name}")
    print()
    
    try:
        # Create client
        client = AsyncIOMotorClient(mongodb_url, serverSelectionTimeoutMS=5000)
        
        # Test connection
        await client.admin.command('ping')
        print("SUCCESS: MongoDB connection successful!")
        print()
        
        # Get database
        db = client[database_name]
        
        # List collections
        collections = await db.list_collection_names()
        print(f"DATA: Database '{database_name}' exists")
        print(f"   Collections: {collections if collections else '(none yet)'}")
        print()
        
        # Check users collection
        users_count = await db.users.count_documents({})
        predictions_count = await db.predictions.count_documents({})
        
        print(f"USERS: Users in database: {users_count}")
        print(f"PREDICTIONS: Predictions in database: {predictions_count}")
        print()
        
        print("SUCCESS: MongoDB is ready to use!")
        
        # Close connection
        client.close()
        return True
        
    except Exception as e:
        print(f"ERROR: MongoDB connection failed!")
        print(f"   Error: {str(e)}")
        print()
        print("Troubleshooting:")
        print("   1. Is MongoDB running? (Check with: Get-Service MongoDB)")
        print("   2. Check your MONGODB_URL in .env file")
        print("   3. For Atlas: Is your IP whitelisted?")
        print("   4. For Atlas: Are username/password correct?")
        print()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("MongoDB Connection Test")
    print("=" * 60)
    print()
    
    success = asyncio.run(test_mongodb_connection())
    
    print("=" * 60)
    sys.exit(0 if success else 1)

