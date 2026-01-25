# Pneumonia Detection using CNN

This project implements a web application for detecting pneumonia from chest X-ray images using a Convolutional Neural Network (CNN).

## Getting Started

Follow these instructions to set up and run the project.

### Prerequisites

*   Python 3.13.7
*   pip (Python package installer)
*   Docker (if you want to run the application using Docker)

### Running the Application Locally

To run the application locally, you can use the provided shell script. This script automates the setup and execution process.

1.  **Navigate to the project root directory:**
    ```bash
    cd /path/to/Pneumonia_detection_using_CNN
    ```

2.  **Run the script:**
    ```bash
    ./run_app.sh
    ```
    This script will:
    *   Navigate to the `Frontend-code/Frontend-vscode` directory.
    *   Create a virtual environment named `env` if it doesn't already exist.
    *   Activate the virtual environment.
    *   Install all the required dependencies from the `requirements.txt` file.
    *   Start the Flask application.
    *   Automatically open the application in your default web browser at `http://127.0.0.1:5000/`.

    The application will be accessible at `http://127.0.0.1:5000/`.

### Building and Running with Docker

To build a Docker image of the application and run it in a container, follow these steps:

1.  **Ensure Docker is installed and running** on your system.

2.  **Navigate to the project root directory:**
    ```bash
    cd /path/to/Pneumonia_detection_using_CNN
    ```

3.  **Build the Docker image:** This command will read the `Dockerfile` and build a Docker image.
    ```bash
    docker-compose build
    ```

4.  **Run the Docker container:** This command will start the application within a Docker container and map port 5000 from the container to port 5000 on your host machine.
    ```bash
    docker-compose up
    ```
    The application will be accessible at `http://localhost:5000/`.

## Detailed Project Structure

*   `Backend_code/`:
    *   `Backend-colab/`: Contains `Final_Pneumonia_detection_using_CNN.ipynb`, which is a Jupyter notebook detailing the development, training, and evaluation of the Convolutional Neural Network model for pneumonia detection.
*   `Frontend-code/`:
    *   `Frontend-vscode/`: This directory houses the Flask web application.
        *   `app.py`: The main Flask application file. It handles web requests, loads the trained CNN model, processes image uploads, makes predictions, and renders HTML templates.
        *   `models/`: Contains the pre-trained Keras model (`pneu_cnn_model.h5`).
        *   `static/`: Stores uploaded images and other static assets.
        *   `templates/`: Contains the `index.html` template.
*   `Dockerfile`: Defines the steps to build a Docker image of the Flask application.
*   `docker-compose.yml`: Configures Docker services.
*   `requirements.txt`: Lists all Python packages required by the project.
*   `run_app.sh`: A shell script to automate the local setup and execution of the Flask application.

## Step-by-step Workflow of the Project

The application follows a straightforward workflow:

1.  **User Interaction**: A user accesses the web application through their browser.
2.  **Image Upload**: The user uploads an X-ray image via the web interface.
3.  **Flask Request Handling**: The `app.py` Flask application receives the uploaded image.
4.  **Image Preprocessing**: The uploaded image is processed and prepared for the model.
5.  **Prediction**: The CNN model predicts the likelihood of pneumonia.
6.  **Result Display**: The classification result, uploaded image, and health insights are rendered back to the `index.html` template and displayed to the user.

## Project Summary

As a key contributor to the Pneumonia Detection web application, I was responsible for transforming a basic proof-of-concept into a full-featured, user-friendly, and robust application. I led a series of significant enhancements, from backend architecture to frontend UI/UX, demonstrating a wide range of full-stack development skills.

### Key Contributions & Accomplishments

*   **Full-Stack Web Application Development:**
    *   Engineered a full-featured web application from a basic script, implementing a database-backed user authentication system, a dynamic user interface, and a machine learning model integration.
    *   Demonstrated architectural flexibility by successfully migrating the application from a server-side rendered Flask app to a decoupled architecture with a Flask REST API and a React.js frontend, and then back again based on changing project requirements.

*   **Backend Development & API Design:**
    *   Re-architected the Flask backend to support a persistent user database using SQLite and Flask-SQLAlchemy.
    *   Implemented a secure, form-based user authentication and session management system with Flask-Login, including password hashing with `werkzeug.security`.
    *   Designed and built a RESTful API with Flask to serve predictions from the CNN model and provide data to a separate frontend.

*   **Frontend Development & UI/UX Design:**
    *   Designed and implemented a modern, responsive, and visually appealing user interface using Bootstrap and advanced CSS, resulting in a "fantastic" user experience.
    *   Created dynamic and engaging UI elements with "production level" hover effects and animations using CSS transitions, transforms, and pseudo-elements.
    *   Enhanced the user experience by providing detailed, data-driven health insights based on the model's prediction score, and by adding a comprehensive information section about pneumonia.

*   **DevOps & Automation:**
    *   Improved the application's robustness and usability by creating a comprehensive shell script (`run_app.sh`) for automated setup, dependency installation, and execution of the application.
    *   Implemented robust process management in the startup script to ensure clean termination of background processes.

*   **Debugging & Problem Solving:**
    *   Successfully diagnosed and resolved a wide range of technical issues, including HTTP errors ("Method Not Allowed"), port conflicts ("Address already in use"), and application startup race conditions.

## Development History

This project has undergone several major updates to improve its functionality, architecture, and user experience.

-   **Initial Setup and Debugging:** Corrected execution scripts and application paths to ensure the application could run reliably.
-   **File Validation:** Implemented robust file validation to ensure that users can only upload valid image files.
-   **Architectural Refactoring:** The application was briefly refactored into a decoupled architecture with a Flask REST API and a React.js frontend, before being reverted to a server-side rendered Flask application based on user feedback.
-   **Database-Backed User Authentication:** Replaced the initial in-memory user store with a persistent SQLite database using Flask-SQLAlchemy and implemented secure password hashing.
-   **Full Signup and Login Flow:** Implemented a full-featured, form-based authentication system with Flask-Login to manage user sessions.
-   **UI/UX Improvements:** The user interface was completely redesigned with a modern, dark theme, advanced hover effects, and a more user-friendly layout. The application was also enhanced to provide more detailed health insights and general information about pneumonia.
-   **Bug-fixing and Robustness:** A variety of bugs and errors were resolved, and the startup script was significantly improved for a better user experience.

For a more detailed, step-by-step documentation of the changes, please see the `updates_documentation.md` file.
