# 🛠️ MongoDB SSL Handshake Error – ECS Deployment Walkthrough

This guide helps troubleshoot and resolve the following error when deploying this FastAPI app to AWS ECS:

```
pymongo.errors.ServerSelectionTimeoutError: SSL handshake failed: ...
```

---

## ❗ Error Description

This error often looks like:

```
SSL handshake failed: ac-xyz.mongodb.net:27017: [SSL: TLSV1_ALERT_INTERNAL_ERROR]
...
TopologyDescription: ReplicaSetNoPrimary, servers: ... error=AutoReconnect
```

This means MongoDB Atlas **rejected the ECS container's connection** because the IP making the request is not on the allowlist.

---

## ✅ Root Cause

MongoDB Atlas **requires all incoming requests** to come from **authorized IP addresses**.

When ECS creates a task, it assigns a **dynamic public IP** (unless you've set a static one). If that public IP isn't added to Atlas's **IP Access List**, the connection fails during the SSL handshake.

---

## 🧭 Step-by-Step Fix

### 1. 🧾 Find Your ECS Task's Public IP

1. Go to the AWS Console.
2. Navigate to: `ECS → Clusters → [your-cluster] → Tasks`
3. Click your running **Task**
4. Under the **"Network"** section, find:

   * **ENI (Elastic Network Interface)**: click to go to EC2
   * Look for **IPv4 Public IP**

> 📌 *Copy this IP address*

---

### 2. 🌐 Add IP to MongoDB Atlas

1. Go to [MongoDB Atlas Console](https://cloud.mongodb.com)
2. Open your **Project → Network Access**
3. Click **“Add IP Address”**
4. Paste the **public IP address**
5. Optionally: give it a name (e.g., `ecs-task-ip`)
6. Save

🕐 Wait \~1–2 minutes for the rule to propagate.

---

### 3. 🔁 Re-run Your Task or Service

Once the IP is allowlisted:

* Re-deploy the service, or
* Re-run your task manually (e.g., `Run Task` from the ECS UI)

If your container logs now show:

```
Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

Then the app has successfully connected to MongoDB 🎉

---

## 🧩 Optional – Make IP Static (Recommended for Stability)

ECS public IPs may change over time. If this is an issue, consider:

### 🔹 Option 1: Assign a **Static Elastic IP**

1. Allocate an **Elastic IP** from EC2
2. Attach it to a **NAT Gateway**
3. Use the NAT in your ECS subnet route table
4. Allow **that single Elastic IP** in MongoDB

### 🔹 Option 2: Use **VPC Peering or AWS PrivateLink**

Advanced setup that avoids public IPs entirely by routing traffic over private networks.

---

## 🚨 Temporary Testing Alternative

If you’re just testing (not production), you can allow all traffic:

```text
0.0.0.0/0
```

> ⚠️ **Do NOT use this in production.** It opens your database to the entire internet.

---

## 🧪 Verifying the Connection

You can confirm MongoDB is reachable by:

* Checking logs: `MongoDB connected successfully`
* Verifying data is created on POST requests
* Using MongoDB Atlas **Data Explorer** to inspect the `taskmgmt` database

---

## 🧼 Clean Up

To avoid charges or exposure:

* Remove unused ECS tasks or services
* Delete `0.0.0.0/0` entries from MongoDB Atlas
* Tear down resources if testing is complete

---

## ✅ Final Checklist

| Task                                   | Status |
| -------------------------------------- | ------ |
| ECS Task has public IP                 | ✅      |
| IP added to MongoDB Atlas              | ✅      |
| Port 80 or 8000 open in security group | ✅      |
| App connects successfully              | ✅      |

---

Let me know if you'd like this saved to a file or formatted for GitHub directly.
