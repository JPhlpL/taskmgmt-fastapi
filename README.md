# 📝 Task Management API

A simple Task Management API built with **FastAPI**, **MongoDB Atlas**, and **Pydantic v2**. It supports basic task creation (CRUD coming soon) with secure header-based authentication.

---

## 🚀 Features

* ✅ Task creation with email and details
* 🔒 Header-based API authentication (`X_AUTH_API_KEY`)
* 🔧 MongoDB Atlas integration via Motor (async)
* 🪵 Rotating file logger (no logfire yet)
* 📦 Pydantic v2 for request/response models
* ⚙️ Scalable architecture (service-repository pattern)

---

## 🖥️ Local Setup

### 1. ✅ Clone the Repository

```bash
git clone https://github.com/yourusername/taskmgmt-api.git
cd taskmgmt-api
```

### 2. 📦 Create and Activate a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3. 📥 Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. ⚙️ Configure Environment
Create a file called .env.local in the root directory:
```bash
MONGO_URI=mongodb+srv://<username>:<password>@<cluster-url>/taskmgmt?retryWrites=true&w=majority
X_AUTH_API_KEY=e33739abbd2a02c2e988d67ebe5a26f865231443a6d3adf57d021e0eeda6ef04299139a24e33c0560640471935392b85d2f4799a0ac87de188d0c06499e82382
```

### 5. ▶️ Run the Server

```bash
uvicorn src.main:app --reload
```

### 🔐 Authorization Header

```bash
X_AUTH_API_KEY: <your_api_key_from_.env.local>
```

### 🧪 Sample cURL Request

```bash
curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -H "X_AUTH_API_KEY: e33739abbd2a02c2e988d67ebe5a26f865231443a6d3adf57d021e0eeda6ef04299139a24e33c0560640471935392b85d2f4799a0ac87de188d0c06499e82382" \
  -d '{"email": "john@example.com", "details": "Finish FastAPI tutorial"}'
```

### 🐳 Docker Setup (Coming Soon)

To run this project in Docker:

Add a Dockerfile and .dockerignore

Mount the .env.local

Use a docker-compose.yml for local Mongo (optional)

📌 A complete Docker-ready config will be added in a future update.

### 🐳 Docker Setup (Coming Soon)

```bash
src/
├── core/          # DB, config, logging
├── models/        # TypedDicts
├── schemas/       # Pydantic request/response schemas
├── services/      # Business logic
├── repositories/  # DB interactions
├── routers/       # FastAPI routes
├── utils/         # Helpers (auth, dependencies)
├── wrappers/      # Retry wrappers (optional)
└── prompts/       # Future: AI prompt templates
```

### 📋 Tasks To-Do

```bash
| Status | Feature                           | Notes                                              |
| ------ | --------------------------------- | -------------------------------------------------- |
| ✅      | `POST /tasks/`                    | Create a task with email and details               |
| ✅      | `GET /tasks/?email=`              | Fetch all tasks for a given email                  |
| ✅      | `PUT /tasks/{id}`                 | Update task by UUID                                |
| ✅      | `DELETE /tasks/{id}`              | Delete task by UUID                                |
| 🕐     | Validation for duplicate tasks    | Prevent creating same task twice (optional)        |
| ⬜      | Pagination for task lists         | `/tasks/?email=abc@example.com&page=1&size=10`     |
| ⬜      | Search/filter by content or date  | Full-text or field filtering                       |
| ⬜      | Mark task as completed/incomplete | Add `status: str` (e.g., pending, done)            |
| ⬜      | Due dates & reminders             | Add `due_date`, `reminder_sent`                    |
| ⬜      | User login/authentication         | JWT or OAuth integration                           |
| ⬜      | Rate limiting / abuse protection  | Prevent spam task creation                         |
| ⬜      | AI Task Suggestions               | Based on user history (future `prompts/`)          |
| ⬜      | Docker & deployment support       | `Dockerfile`, `docker-compose.yml`, `.env support` |
```
