# 🧭 ECS Deployment Walkthrough for FastAPI + MongoDB Atlas

---

## ✅ **Step 1: Prerequisites**

### Tools you need:

* ✅ AWS account
* ✅ Docker installed
* ✅ AWS CLI configured (`aws configure`)
* ✅ MongoDB Atlas cluster with connection string
* ✅ FastAPI project with working `Dockerfile`

---

## 🐳 Step 2: Dockerize Your App

In the root of your project, add this `Dockerfile`:

```Dockerfile
# Use an official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Expose the port
EXPOSE 80

# Start Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
```

Create a `.dockerignore` file too:

```
__pycache__/
.venv/
.env.local
*.pyc
```

---

## 📁 Step 3: Push to Amazon ECR

### 1. **Create ECR Repo**

```bash
aws ecr create-repository --repository-name taskmgmt-api
```

### 2. **Authenticate Docker with ECR**

```bash
aws ecr get-login-password | docker login --username AWS --password-stdin <your_aws_account_id>.dkr.ecr.<region>.amazonaws.com
```

### 3. **Build and Push Image**

```bash
docker build -t taskmgmt-api .
docker tag taskmgmt-api:latest <your_aws_account_id>.dkr.ecr.<region>.amazonaws.com/taskmgmt-api
docker push <your_aws_account_id>.dkr.ecr.<region>.amazonaws.com/taskmgmt-api
```

---

## 🚀 Step 4: Create ECS Fargate Cluster

1. Go to **ECS > Clusters** → "Create Cluster"
2. Choose **"Networking only" (Fargate)**
3. Name it `taskmgmt-cluster`
4. Create

---

## 🔧 Step 5: Define a Task Definition

1. Go to **ECS > Task Definitions**
2. Click **Create new Task Definition** → Choose **Fargate**
3. Fill in:

   * Task Name: `taskmgmt-task`
   * Task role: leave blank (or custom role if needed)
   * **Container Name**: `taskmgmt-container`
   * **Image**: your pushed ECR image URL
   * **Port mappings**: container port `80`
4. **Environment variables (VERY IMPORTANT)**:

   * Add:

     ```
     MONGO_URI = your mongodb+srv:// connection string
     X_AUTH_API_KEY = your long API key
     ```
5. Click **Create**

---

## 🌐 Step 6: Create a Service

1. Go to **ECS > Clusters > taskmgmt-cluster**
2. Click **Create Service**
3. Launch type: Fargate
4. Task Definition: pick `taskmgmt-task`
5. Desired tasks: 1
6. **Networking**:

   * Pick VPC and subnets
   * Assign **public IP**
   * Select or create a **Security Group**

     * Inbound rule: allow TCP on port **80** from `0.0.0.0/0` (public)

Click **Create Service**

---

## 🌍 Step 7: Test It!

1. Once the task is running, go to **EC2 > Network Interfaces**
2. Find the **Public IP** of your running task
3. Visit: `http://<public-ip>/tasks/`

---

## 🧪 Sample cURL Test

```bash
curl -X POST http://<public-ip>/tasks/ \
  -H "Content-Type: application/json" \
  -H "X_AUTH_API_KEY: your_api_key" \
  -d '{"email": "test@example.com", "details": "Deploy to ECS"}'
```

---

## 🛠️ Troubleshooting Tips

| Problem                         | Fix                                                                                      |
| ------------------------------- | ---------------------------------------------------------------------------------------- |
| `Connection refused` or timeout | Make sure the task has a **public IP**, and **port 80** is allowed in the security group |
| FastAPI shows 8000              | Change `--port 8000` to `--port 80` in `CMD` of Dockerfile                               |
| Task won’t run                  | Check logs in ECS → Tasks → View logs                                                    |
| Secret not working              | Make sure `MONGO_URI` and `X_AUTH_API_KEY` are **set as env vars in task definition**    |

---

## 🔐 Security Notes

* Use **HTTPS** via Load Balancer + SSL cert (ACM)
* Restrict IPs instead of `0.0.0.0/0` for production
* Never push `.env.local` to GitHub

---

## ✅ Summary

You’ve now:

* 🐳 Dockerized the FastAPI app
* ☁️ Deployed to AWS ECS with MongoDB Atlas
* 🔐 Secured with header auth
* 📡 Exposed via public IP on port 80

---

Let me know if you want:

* ✅ A `docker-compose.yml` for local MongoDB
* ✅ Full CRUD endpoints
* ✅ GitHub Actions for ECS deployment

Happy building! 🚀
