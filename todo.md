**Ongoing:**
1. Make a simple chatbot with AI integration
2. Make a prefix for all logging
3. Reupload this again on modal
4. make taskmgmt_username and password more robust


**Some Tasks**
```bash
| Status | Feature                           | Notes                                              |
| ------ | --------------------------------- | -------------------------------------------------- |
| ✅      | `POST /tasks/`                    | Create a task with email and details               |
| ✅      | `GET /tasks/?email=`              | Fetch all tasks for a given email                  |
| ✅      | `PUT /tasks/{id}`                 | Update task by UUID                                |
| ✅      | `DELETE /tasks/{id}`              | Delete task by UUID                                |
| 🕐     | Validation for duplicate tasks    | Prevent creating same task twice (optional)        |
| 🕐     | Add LogFire                       | Logstream Proper                                   |
| ⬜      | User login/authentication         | JWT or OAuth integration                           |
| ⬜      | Pagination for task lists         | `/tasks/?email=abc@example.com&page=1&size=10`     |
| ⬜      | Search/filter by content or date  | Full-text or field filtering                       |
| ⬜      | Mark task as completed/incomplete | Add `status: str` (e.g., pending, done)            |
| ⬜      | Due dates & reminders             | Add `due_date`, `reminder_sent`                    |
| ⬜      | Rate limiting / abuse protection  | Prevent spam task creation                         |
| ⬜      | AI Task Suggestions               | Based on user history (future `prompts/`)          |
| ⬜      | Docker & deployment support       | `Dockerfile`, `docker-compose.yml`, `.env support` |
```