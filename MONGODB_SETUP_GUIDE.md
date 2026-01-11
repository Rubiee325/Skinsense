# MongoDB Setup Guide for SkinMorph

This guide will help you set up MongoDB for the SkinMorph application on Windows.

---

## 🚀 Option 1: MongoDB Atlas (Cloud - Easiest & Free)

**Best for:** Quick setup, no local installation needed, free tier available

### Steps:

1. **Sign up for MongoDB Atlas** (Free tier)
   - Go to: https://www.mongodb.com/cloud/atlas/register
   - Create a free account

2. **Create a Free Cluster**
   - Click "Build a Database"
   - Choose "M0 FREE" tier
   - Select a cloud provider and region (choose closest to you)
   - Click "Create"

3. **Create Database User**
   - Go to "Database Access" (left sidebar)
   - Click "Add New Database User"
   - Choose "Password" authentication
   - Username: `skinmorph_user` (or any name)
   - Password: Create a strong password (save it!)
   - Database User Privileges: "Read and write to any database"
   - Click "Add User"

4. **Configure Network Access**
   - Go to "Network Access" (left sidebar)
   - Click "Add IP Address"
   - For development: Click "Allow Access from Anywhere" (0.0.0.0/0)
   - For production: Add your specific IP addresses
   - Click "Confirm"

5. **Get Connection String**
   - Go to "Database" (left sidebar)
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Driver: "Python"
   - Version: "3.6 or later"
   - Copy the connection string (looks like: `mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority`)

6. **Update Your Environment Variables**
   Create a `.env` file in the `backend` directory:
   ```bash
   MONGODB_URL=mongodb+srv://skinmorph_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   MONGODB_DATABASE=skinmorph
   JWT_SECRET_KEY=your-secret-key-change-this-in-production-12345
   ```
   
   Replace:
   - `YOUR_PASSWORD` with your actual database user password
   - `cluster0.xxxxx.mongodb.net` with your actual cluster URL

7. **Install python-dotenv** (if not already installed)
   ```powershell
   pip install python-dotenv
   ```

8. **Update db.py to load from .env** (if needed)
   The code already reads from environment variables, so it should work!

---

## 💻 Option 2: Install MongoDB Community Server (Local)

**Best for:** Full control, offline development, no internet needed after setup

### Steps:

1. **Download MongoDB Community Server**
   - Go to: https://www.mongodb.com/try/download/community
   - Version: Latest (7.0 or newer recommended)
   - Platform: Windows
   - Package: MSI
   - Click "Download"

2. **Install MongoDB**
   - Run the downloaded `.msi` file
   - Choose "Complete" installation
   - Check "Install MongoDB as a Service"
   - Service Name: `MongoDB` (default)
   - Service Account: "Run service as Network Service user" (default)
   - Check "Install MongoDB Compass" (optional GUI tool)
   - Click "Install"

3. **Verify Installation**
   - MongoDB should be running automatically as a Windows service
   - Open Command Prompt or PowerShell as Administrator:
     ```powershell
     # Check if MongoDB service is running
     Get-Service MongoDB
     
     # If not running, start it:
     Start-Service MongoDB
     ```

4. **Test MongoDB Connection**
   ```powershell
   # Connect to MongoDB shell
   mongosh
   
   # Or if mongosh is not in PATH, use:
   "C:\Program Files\MongoDB\Server\7.0\bin\mongosh.exe"
   ```
   
   If connected, you should see: `test>`

5. **Configure Your Application**
   Create a `.env` file in the `backend` directory:
   ```bash
   MONGODB_URL=mongodb://localhost:27017
   MONGODB_DATABASE=skinmorph
   JWT_SECRET_KEY=your-secret-key-change-this-in-production-12345
   ```

6. **Verify MongoDB is Running**
   ```powershell
   # Test connection from Python
   python -c "from motor.motor_asyncio import AsyncIOMotorClient; import asyncio; async def test(): client = AsyncIOMotorClient('mongodb://localhost:27017'); await client.admin.command('ping'); print('MongoDB connected!'); asyncio.run(test())"
   ```

---

## 🐳 Option 3: Docker (If you install Docker Desktop)

**Best for:** Isolated containers, easy cleanup, consistent across environments

### Steps:

1. **Install Docker Desktop for Windows**
   - Download from: https://www.docker.com/products/docker-desktop/
   - Install and restart your computer
   - Start Docker Desktop

2. **Run MongoDB Container**
   ```powershell
   docker run -d -p 27017:27017 --name mongodb -v mongodb_data:/data/db mongo:latest
   ```

3. **Verify Container is Running**
   ```powershell
   docker ps
   ```
   Should show `mongodb` container running

4. **Stop/Start Container** (when needed)
   ```powershell
   # Stop
   docker stop mongodb
   
   # Start
   docker start mongodb
   
   # Remove container (if needed)
   docker rm mongodb
   ```

5. **Configure Your Application**
   Same as Option 2 - use `mongodb://localhost:27017`

---

## 🔧 Troubleshooting

### MongoDB Service Not Starting (Option 2)

**Error:** "MongoDB service failed to start"

**Solution:**
```powershell
# Run PowerShell as Administrator
Get-Service MongoDB
Start-Service MongoDB

# If it fails, check logs:
Get-EventLog -LogName Application -Source MongoDB -Newest 10
```

### Connection Refused

**Error:** "Failed to connect to MongoDB"

**Check:**
1. Is MongoDB running? (`Get-Service MongoDB` or `docker ps`)
2. Is port 27017 available? (`netstat -an | findstr 27017`)
3. Check firewall settings
4. Verify connection string in `.env` file

### Authentication Failed (Atlas)

**Error:** "Authentication failed"

**Solution:**
1. Verify username and password in connection string
2. Check if IP is whitelisted in Atlas Network Access
3. URL-encode special characters in password (e.g., `@` becomes `%40`)

---

## ✅ Quick Test

After setup, test your MongoDB connection:

```powershell
cd backend
python -c "import asyncio; from motor.motor_asyncio import AsyncIOMotorClient; import os; from dotenv import load_dotenv; load_dotenv(); async def test(): client = AsyncIOMotorClient(os.getenv('MONGODB_URL', 'mongodb://localhost:27017')); await client.admin.command('ping'); print('✅ MongoDB connected successfully!'); asyncio.run(test())"
```

Or test with the actual app:
```powershell
cd backend
uvicorn app.main:app --reload
# Then visit http://localhost:8000/health
```

---

## 📝 Next Steps After MongoDB Setup

1. ✅ MongoDB is running
2. ✅ Environment variables are set (`.env` file)
3. ✅ Start your FastAPI app:
   ```powershell
   cd backend
   uvicorn app.main:app --reload
   ```
4. ✅ Test signup:
   ```powershell
   curl -X POST "http://localhost:8000/auth/signup" -H "Content-Type: application/json" -d '{"email":"test@example.com","password":"test123","name":"Test User","age":25,"gender":"male"}'
   ```

---

## 🌐 MongoDB Atlas Connection String Format

For MongoDB Atlas, your connection string should look like:
```
mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

Replace:
- `username` - Your database user username
- `password` - Your database user password (URL-encode special chars)
- `cluster0.xxxxx.mongodb.net` - Your actual cluster URL

Example `.env` file for Atlas:
```bash
MONGODB_URL=mongodb+srv://skinmorph_user:MyP@ssw0rd123@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority
MONGODB_DATABASE=skinmorph
JWT_SECRET_KEY=super-secret-key-change-in-production-987654321
```

---

**Recommended for beginners:** Start with **MongoDB Atlas (Option 1)** - it's free, no installation needed, and works immediately! 🚀

