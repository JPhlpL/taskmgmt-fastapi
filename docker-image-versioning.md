# 🚀 Deploying Refactored FastAPI App to AWS ECS with Versioning

This guide assumes:

* You're using **Docker** for your FastAPI app
* You've already set up an ECS cluster
* You’re pushing images to **Amazon ECR (Elastic Container Registry)**

---

## ✅ 1. Refactor Your Code Locally

Before deploying:

* Make sure all changes are committed and tested locally
* Update `.env`, `Dockerfile`, or any configs accordingly

---

## 🛠 2. Build a Versioned Docker Image

To support **rollbacks** and **version tracking**, tag each Docker image with a version.

### Example:

```bash
docker build -t taskmgmt-api:v1.0.0 .
```

You can use:

* `v1.0.0`, `v1.1.0` (semantic versioning)
* or a date-based version `2025-06-25`

---

## 📦 3. Push to Amazon ECR

### First, authenticate to ECR:

```bash
aws ecr get-login-password --region your-region | docker login --username AWS --password-stdin [your_account_id].dkr.ecr.[region].amazonaws.com
```

### Tag the image for ECR:

```bash
docker tag taskmgmt-api:v1.0.0 [your_account_id].dkr.ecr.[region].amazonaws.com/taskmgmt-api:v1.0.0
```

### Push to ECR:

```bash
docker push [your_account_id].dkr.ecr.[region].amazonaws.com/taskmgmt-api:v1.0.0
```

✅ Now you have a **versioned image** stored and ready for ECS.

---

## ⚙️ 4. Update ECS Task Definition

### Open ECS → Task Definitions → Your task

* Click **“Create new revision”**
* In the container section, update the image to:

```text
[your_account_id].dkr.ecr.[region].amazonaws.com/taskmgmt-api:v1.0.0
```

* Add/update environment variables if needed (e.g., `MONGO_URI`, `X_AUTH_API_KEY`)
* Save the new revision

✅ **Every new revision acts like a version snapshot**.

---

## 🚀 5. Update Service to Use New Version

### ECS → Clusters → Services → Your service

* Click **Update**
* In the task definition section, choose the **latest revision**
* Click **Next → Next → Update Service**

This will trigger a **rolling update** using the new image.

---

## 🔁 6. Rollback Support

If something breaks, you can rollback by:

1. ECS → Task Definitions → Choose an older revision
2. ECS → Clusters → Services → Update Service → Select the older revision

Or just deploy an older Docker image version like:

```bash
taskmgmt-api:v0.9.9
```

---

## 🧪 7. Verify the Deployment

* Check service logs
* Try accessing via the **public IP or Load Balancer**
* Test endpoints

---

## 💸 8. Cost-Saving Tips for Personal Use

To minimize charges:

### ✅ Free Tier Benefits

* ECS (Fargate) offers **750 hours/month** for free (for new accounts)
* ECR has a free tier with **500 MB storage/month**

### 💡 Tips:

| Area            | Cost Control Tip                                |
| --------------- | ----------------------------------------------- |
| **ECS Service** | Stop unused services/tasks                      |
| **ECR Storage** | Remove old images                               |
| **Logs**        | Reduce CloudWatch retention                     |
| **Ingress**     | Don’t use expensive load balancers              |
| **Database**    | Use free-tier MongoDB Atlas & allow only ECS IP |

---

## 🧭 Optional – Automate with `copilot` or `CDK`

For advanced deployments:

* Use [AWS Copilot CLI](https://aws.github.io/copilot-cli/) to streamline ECS setups
* Or Infrastructure-as-Code with [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/home.html)

---

## ✅ Summary Checklist

| Step                                          | Status |
| --------------------------------------------- | ------ |
| Refactored and tested app locally             | ✅      |
| Docker image built and tagged (e.g. `v1.0.0`) | ✅      |
| Image pushed to ECR                           | ✅      |
| ECS task definition updated                   | ✅      |
| ECS service updated to latest revision        | ✅      |
| Public IP or Load Balancer tested             | ✅      |
| MongoDB Atlas IP allowlisted                  | ✅      |
