# Contributing to VaultML CE

First off, thank you for considering contributing to **VaultML CE** 💡  
This project is free software under the GNU AGPL v3 (or later) and thrives on community input.

---

## 🛠 How to Contribute

We welcome:

- Bug reports and fixes
- Documentation improvements
- Feature proposals and implementations
- Discussions and design ideas

Please open an **Issue** or **Pull Request** (PR) to start contributing.

---

## 📜 Contributor License Agreement (CLA)

By contributing to VaultML CE, you agree to the **Contributor License Agreement (CLA)**:  

- All copyright in your contributions is **assigned to All-Day Developer**.  
- This ensures VaultML CE can remain open-source while allowing VaultML EE (Enterprise Edition) to exist as a commercial offering.  
- You always retain the right to use your own contributions independently.

The full CLA is available here: [CONTRIBUTOR-LICENSE-AGREEMENT.md](./CONTRIBUTOR-LICENSE-AGREEMENT.md).

---

## ™ Trademark Policy

The names **VaultML**, **VaultML CE**, **VaultML EE**, and the VaultML logos are trademarks of **All-Day Developer, Marcin Wawrzków**.  

Forks and derivatives are welcome under AGPLv3, but you **cannot**:

- Use the name *VaultML* as the primary name of your fork
- Reuse the VaultML logos in a way that implies official support or endorsement

See the full [TRADEMARK-POLICY.md](./TRADEMARK-POLICY.md) for details.

---

## ✅ Commit Requirements

All commits in a Pull Request must be **signed off** with the `Signed-off-by:` line.  
This certifies that you have the rights to contribute under the CLA.

### How to sign off a commit

When committing, use the `-s` flag:

```bash
git commit -s -m "Fix bug in registry API"
```

This adds the line automatically:

```
Signed-off-by: Your Name <your.email@example.com>
```

### CI Enforcement

- **Forked PRs** must pass the **sign-off check** (via `scripts/verify-signoff.sh`).  
- Internal commits (by maintainers) are exempt from this requirement.

If your PR fails the check, you can fix it by rebasing:

```bash
git rebase -i origin/main
# mark commits as 'edit'
git commit --amend -s
git rebase --continue
git push --force-with-lease
```

---

## 🧪 Development Setup

### Prerequisites

- **Docker** and **Docker Compose**
- **Python 3.11+** with pip
- **Node.js 20+** with pnpm
- **Git** with signing configured

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/All-Day-Developer/VaultML-CE.git
   cd VaultML-CE
   ```

2. **Start infrastructure services**
   ```bash
   docker-compose up -d postgres minio
   ```

3. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your local configuration
   ```

### Backend Development

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Source environment variables and run the FastAPI server**
   ```bash
   # Source .env file to export all variables
   set -a && source .env && set +a
   
   # Run the server
   python -m app.server
   # Server available at http://localhost:8000
   ```

3. **API Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Frontend Development

1. **Install dependencies**
   ```bash
   cd frontend
   pnpm install
   ```

2. **Start development server**
   ```bash
   pnpm dev
   # Frontend available at http://localhost:3000
   ```

3. **Build for production**
   ```bash
   pnpm build
   pnpm preview
   ```

### Running Tests

```bash
# Backend tests (when available)
python -m pytest

# Frontend tests (when available)
cd frontend && pnpm test

# Integration tests with Docker
docker-compose -f docker-compose.test.yml up --build
```

### Code Quality

1. **Python formatting**
   ```bash
   black app/
   isort app/
   flake8 app/
   ```

2. **Frontend linting**
   ```bash
   cd frontend
   pnpm lint
   pnpm lint:fix
   ```

---

## 🎯 Contributing Guidelines

### Issue Reporting

When reporting issues, please include:

- **Environment details** (OS, Python version, Node.js version, Docker version)
- **Steps to reproduce** the problem
- **Expected vs actual behavior**
- **Logs and error messages**
- **Screenshots** (for UI issues)

### Pull Request Process

1. **Fork the repository** and create a feature branch
2. **Make your changes** following our coding standards
3. **Add tests** for new functionality
4. **Update documentation** if needed
5. **Sign your commits** with `git commit -s`
6. **Create a pull request** with a clear description

### Coding Standards

#### Backend (Python)
- Follow **PEP 8** style guidelines
- Use **type hints** for function parameters and returns
- Write **docstrings** for modules, classes, and functions
- Keep functions **small and focused**
- Use **async/await** for I/O operations

#### Frontend (TypeScript/Vue)
- Use **TypeScript** strictly (no `any` types)
- Follow **Vue 3 Composition API** patterns
- Use **Pinia** for state management
- Keep components **small and reusable**
- Follow **Tailwind CSS** utility classes

#### Database
- Write **reversible migrations**
- Use **descriptive names** for tables and columns
- Add **proper indexes** for query performance
- Follow **PostgreSQL naming conventions**

### Project Structure

```
app/
├── main.py           # SQLAlchemy models
├── routes.py         # API endpoint definitions
├── server.py         # FastAPI application setup
└── s3.py            # S3/MinIO integration

frontend/app/
├── components/       # Reusable Vue components
├── layouts/         # Page layouts
├── middleware/      # Route middleware
├── pages/           # File-based routing
├── stores/          # Pinia state stores
└── utils/           # Utility functions
```

### Testing

- **Unit tests** for business logic
- **Integration tests** for API endpoints
- **Component tests** for Vue components
- **E2E tests** for critical user flows

### Documentation

- Update **README.md** for new features
- Add **inline code comments** for complex logic
- Update **API documentation** (OpenAPI)
- Write **migration guides** for breaking changes

---

## 🏢 Enterprise Edition

VaultML CE is free software.  
For **enterprise support, commercial licensing, or advanced features**, please contact:

📧 **<marcin.wawrzkow@alldaydev.com>**

---

Thank you for contributing to VaultML CE! 🙌
