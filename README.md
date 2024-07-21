# AZURE FUNCTIONS WITH POSTGRESQL (PYTHON)

## Repository Description

This repository contains a project that integrates Azure Functions with a PostgreSQL database using Python. It provides a set of API endpoints for managing a list of people, demonstrating how to deploy and run serverless functions with database connectivity on Azure.

## Prerequisites

- Familiarity with fundamental API concepts
- An Azure account with an active subscription
- Azure CLI version 2.4 or later
- Docker
- Azure Functions Core Tools
- Azure Functions extension for VS Code

## Environment Variables

Three configuration files are required:

- `.env` in the project root for Docker
- `.env` in the `frontend` folder
- `local.settings.json` in the `api` folder for Azure Functions

Examples of these files are provided in the repository.

## Steps to Run the Project

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. **Start the PostgreSQL database:**

   In the project root, run:

   ```bash
   docker-compose up
   ```

   Customize the database credentials in the `docker-compose.yml` file via `.env` or directly.

   For Linux:

   Create a folder called `pgdata` in the project root:

   ```bash
   mkdir pgdata
   ```

   Change the permissions of the folder called `pgdata` (docker volume) and set the user and group of the folder to 1001:

   ```bash
   sudo chown -R 1001:1001 pgdata
   ```

3. **Set up Azure Functions:**

   Navigate to the `api` folder and install dependencies:

   Create a Python virtual environment in the project root, run:

   ```bash
   cd api
   python3 -m venv ./venv
   source ./venv/bin/activate
   ```

4. **Install the Python dependencies:**

   From the `api` folder, run:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

   For the initial setup, deploy the functions to Azure by following these steps:

   Press `Fn + F5` to deploy the functions, or run the following command in the terminal:

   ```bash
   func start
   ```

   Follow the prompts to configure and debug the functions locally.

5. **Access the application:**

   Open a browser and navigate to `http://localhost:7071/api/hello` to see the message "Hello, World!".

## API Endpoints

- **add_people:** [GET] `http://localhost:7071/api/add_people`
- **add_test_user:** [GET] `http://localhost:7071/api/add_test_user`
- **delete_people:** [DELETE] `http://localhost:7071/api/drop_people`
- **get_people:** [GET] `http://localhost:7071/api/people`
- **hello:** [GET, POST] `http://localhost:7071/api/hello`
- **validate_user:** [POST] `http://localhost:7071/api/validate_user`

## Testing and Usage

- Use Postman or any other API testing tool to test the endpoints.
- Enter your name to see it reflected, indicating the endpoint is working.
- Click the "Populate Data" button to insert sample data of 5 people into the database.
- Click the "Delete Data" button to remove the data.
- Click the "View Data" button to view the data.

## Tests via Postman :

[Postman Collection](https://elements.getpostman.com/redirect?entityId=27211746-2b090b22-f910-4ec4-8b28-3e5648894f6a&entityType=collection)

This guide provides the steps needed to clone the repository, set up the PostgreSQL database, configure Azure Functions, and access the API endpoints for testing and usage.
