# Contributing to OpsPulse

Thank you for your interest in contributing to **OpsPulse**! We are committed to fostering an open, inclusive, and collaborative community.

---

## 🛠️ Development Workflow

1. **Fork & Clone**: Fork the repository on GitHub and clone your fork locally.
2. **Branching**: Always create a descriptive topic branch off `master`:
   ```bash
   git checkout -b feat/add-slack-webhook
   ```
3. **Commit Conventions**: We strictly enforce [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat(telemetry): add disk IOPS metric ingestion`
   - `fix(auth): prevent token refresh race condition`
   - `docs(readme): clarify Docker Compose setup instructions`
   - `refactor(ui): extract chart card to reusable component`

---

## 🧪 Testing & Code Standards

### Backend (Python/Django)
- Ensure all tests pass: `pytest`
- Format and lint code with [Ruff](https://astral.sh/ruff):
  ```bash
  ruff check .
  ruff format --check .
  ```

### Frontend (Next.js/TypeScript)
- Verify TypeScript types without errors:
  ```bash
  npm run build
  ```
- Format with Prettier and ESLint.

---

## 📬 Submitting a Pull Request

1. Push your branch to your fork:
   ```bash
   git push -u origin feat/your-feature
   ```
2. Open a Pull Request against `master`.
3. Provide a clear summary answering **What** changed, **Why**, and include testing evidence.
4. Ensure all GitHub Actions CI checks pass.
