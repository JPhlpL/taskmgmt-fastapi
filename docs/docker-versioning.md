# To-Do
> ** We need to have a specific ip dedicated for each time that we push an image
> ** I noticed that every time revision, the ip address also changes
> ** Make a CI/CD pipeline for automatically deploying the new image version with proper tag definition until it selects to the new revision

# 🚀 ECS Deployment Guide with Semantic + Date-Based Versioning

> ✅ **Current Version:** `taskmgmt-api:v0.0.1-20250701`
> 🗂 **Format:** `taskmgmt-api:v[semver]-[YYYYMMDD]`
> 📦 **Repository:** `taskmgmt-api`

---

## 🔐 Step 0: Authenticate Docker to AWS ECR

```bash
aws ecr get-login-password --region [region] \
| docker login --username AWS --password-stdin [your_account_id].dkr.ecr.[region].amazonaws.com
```

> Replace `[region]` and `[your_account_id]` with your actual AWS region and account ID.

---

## 🛠 Step 1: Build Docker Image with Version Tag

```bash
docker build -t [your_account_id].dkr.ecr.[region].amazonaws.com/taskmgmt-api:v0.0.1-20250701 .
```

> Make sure you're in the project root (where the Dockerfile is).

---

## 📤 Step 2: Push Docker Image to AWS ECR

```bash
docker push [your_account_id].dkr.ecr.[region].amazonaws.com/taskmgmt-api:v0.0.1-20250701
```

You can verify this in the AWS Console:

> **ECR > Repositories > `taskmgmt-api` > Image Tags**

---

## 🧱 Step 3: Register New ECS Task Definition Revision through AWS Console

1. Go to **ECS > Task Definitions**

2. Select `taskmgmt-api`

3. Click **"Create new revision"**

4. In the **Container definitions** section, update the **Image** to:

   ```
   [your_account_id].dkr.ecr.[region].amazonaws.com/taskmgmt-api:v0.0.1-20250701
   ```

5. Leave other settings the same → Click **"Create"**

---

## 🚦 Step 4: Deploy New Task Definition via ECS Service through AWS Console

1. Go to **ECS > Clusters > Your Cluster (e.g., `taskmgmt-api-cluster`)**
2. Click **“Services”**
3. Select your ECS service
4. Click **“Update”**
5. Choose the latest task definition revision
6. Click **“Next”** → **“Next”** → **“Update Service”**

ECS will deploy new tasks using the updated image and gracefully replace the old ones.

---

## 🔍 Step 5: Verify Your Deployment

* Go to the **"Tasks"** tab under your ECS service
* Ensure your task is in **"Running"** state with the latest revision
* Visit the **Public IP** or **DNS name** of your EC2 instance or Load Balancer

---

## 📦 Optional: Automate the Workflow (CI/CD)

You can automate the entire process:

* **Build & push Docker image** on every commit or tag
* **Update ECS service** using:

```bash
aws ecs update-service \
  --cluster [your-cluster-name] \
  --service [your-service-name] \
  --task-definition taskmgmt-api
```
