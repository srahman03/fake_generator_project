# JSON Schema Test Data Generator

A Python-based project that generates test data from a given JSON schema. The project exposes a web API to access the functionality, with a CI/CD pipeline for automated builds and deployment.

## Features

- **JSON Schema Input:** Accepts a JSON schema and generates test data accordingly.  
- **Python API:** Handles the logic for data generation.  
- **Web API:** Access the Python API over HTTP.  
- **Dockerized Deployment:** Uses Docker Compose for easy setup and containerization.  
- **CI/CD Integration:** Automated builds and deployments using Jenkins pipeline on code commits.  
- **Gunicorn & Nginx:** Production-ready deployment with Gunicorn as the WSGI server and Nginx as reverse proxy.  
- **ELK Integration:** Generated test data can be sent to Elasticsearch for further processing and visualization with the ELK stack.  
- **AWS EC2 Deployment:** Tested on EC2 instance and locally.  

## Tech Stack

- **Backend:** Python  
- **API Server:** Flask/FastAPI (assuming) + Gunicorn  
- **Web Server:** Nginx  
- **Containerization:** Docker & Docker Compose  
- **CI/CD:** Jenkins  
- **Database/Logging:** Elasticsearch (ELK Stack)  
- **Deployment:** AWS EC2  


## Installation & Setup
1. Install Docker:

- Install Docker

2. Clone the repository:

```bash
git clone <your-repo-url>
cd <your-project-directory>
```

3. Running the app

- docker compose up 
