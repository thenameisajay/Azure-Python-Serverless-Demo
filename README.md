# Azure Functions with PostgreSQL (Python)

## Repository Overview

This repository showcases a project integrating Azure Functions with a PostgreSQL database using Python. It provides a suite of API endpoints to manage a list of people, demonstrating the deployment and execution of serverless functions with database connectivity on Azure.

## Prerequisites

To successfully run this project, ensure you have the following:

- Knowledge of basic API concepts
- An active Azure subscription
- Azure CLI version 2.4 or later
- Docker
- Azure Functions Core Tools
- Azure Functions extension for VS Code
- Python 3 (preferably 3.11.xx)

## Environment Configuration

You will need the following configuration files:

- `.env` in the project root for Docker
- `.env` in the `frontend` folder
- `local.settings.json` in the `api` folder for Azure Functions

Sample configuration files are included in the repository.

## Setup Instructions

Follow these steps to set up and run the project:

1. **Clone the Repository**

   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. **Start the PostgreSQL Database**

   In the project root, execute:

   ```bash
   docker-compose up
   ```

   Customize the database credentials in the `docker-compose.yml` file or directly via the `.env` file.

   For Linux users:

   Create a `pgdata` directory in the project root:

   ```bash
   mkdir pgdata
   ```

   Change the permissions and set the user and group of the `pgdata` directory to 1001:

   ```bash
   sudo chown -R 1001:1001 pgdata
   ```

3. **Set Up Azure Functions**

   Create a Python virtual environment in the project root and activate it:

   ```bash
   python3 -m venv ./venv
   source ./venv/bin/activate
   ```

4. **Install Python Dependencies**

   From the project root, run:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

5. **Deploy and Run Azure Functions**

   For the initial setup, deploy the functions to Azure by following these steps:

   - Press `Fn + F5` to deploy the functions, or run the following command in the terminal:

     ```bash
     func start
     ```

   - Follow the prompts to configure and debug the functions locally.

6. **Access the Application**

   Open a browser and navigate to `http://localhost:7071/api/hello` to see the message "Hello, World!".

## API Endpoints

The following API endpoints are available:

- **add_people:** [GET] `http://localhost:7071/api/add_people`
- **add_test_user:** [GET] `http://localhost:7071/api/add_test_user`
- **delete_people:** [DELETE] `http://localhost:7071/api/drop_people`
- **get_people:** [GET] `http://localhost:7071/api/people`
- **hello:** [GET, POST] `http://localhost:7071/api/hello`
- **validate_user:** [POST] `http://localhost:7071/api/validate_user`
- **add_user:** [POST] `http://localhost:7071/api/add_user`

## Testing and Usage

- Use Postman or another API testing tool to test the endpoints.
- Send a [POST] request with your name to the `/api/hello` endpoint to verify functionality.
- Use the "Populate Data" button to insert five people's sample data into the database.
- Use the "Delete Data" button to remove the data.
- Use the "View Data" button to view the data.

## Testing with Postman

A Postman collection is available for testing the API endpoints:

[Postman Collection](https://elements.getpostman.com/redirect?entityId=27211746-2b090b22-f910-4ec4-8b28-3e5648894f6a&entityType=collection)

This guide outlines the steps to clone the repository, set up the PostgreSQL database, configure Azure Functions, and access the API endpoints for testing and usage.
