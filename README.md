# Resume as Code 🚀

![Build Status](https://img.shields.io/github/actions/workflow/status/giorgi-dundua/dundua-dev-cv/fly-deploy.yml?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Docker](https://img.shields.io/badge/Docker-Container-blue?style=flat-square&logo=docker)

A data-driven, containerized personal portfolio and CV platform. 
Live at **[dundua.dev](https://dundua.dev)**.

## 🏗 Architecture

This is not a static HTML page. It is a dynamic Flask application designed to demonstrate **DevOps** and **Backend** best practices:

*   **Source of Truth:** CV data is separated from presentation logic (`cv_data.json`).
*   **Privacy by Design:** Sensitive data (phone number) is injected via a local-only `secrets.json` overlay, ensuring it never hits the public repository or the production cloud environment.
*   **CI/CD:** Automated deployment pipeline via **GitHub Actions**.
*   **Infrastructure:** Dockerized runtime hosted on **Fly.io** (Firecracker microVMs).
*   **Print Optimization:** Custom CSS print media queries transform the responsive web view into a strict A4 document for PDF generation.

## 🛠 Local Development

1.  **Clone the repo**
    ```bash
    git clone https://github.com/giorgi-dundua/dundua-dev-cv.git
    cd dundua-dev-cv
    ```

2.  **Setup Environment**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Add Private Data (Optional)**
    Create a `secrets.json` file in the root to override public fields:
    ```json
    {
      "basics": {
        "phone": "+46 70 123 45 67"
      }
    }
    ```

4.  **Run**
    ```bash
    python run.py
    ```
    Visit `http://localhost:8080`.

## 🐳 Docker Build

```bash
docker build -t cv-app .
docker run -p 8080:8080 cv-app