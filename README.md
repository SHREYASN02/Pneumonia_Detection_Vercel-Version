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
    *   Check if a virtual environment named `.venv` exists. If not, it will create one and install all the required dependencies from `requirements.txt`.
    *   Navigate to the `Frontend-code/` directory.
    *   Activate the virtual environment.
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
*   `.venv/`: (New) Python virtual environment created for local development (not included in version control).

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

## Detailed Update History
# Project Updates Documentation

This document outlines the step-by-step updates and improvements made to the Pneumonia Detection web application.

## 1. Initial Setup and Debugging

-   **Corrected Execution Script:** The initial `run_app.sh` script was debugged to correct pathing issues that prevented the application from starting correctly.
-   **Fixed Application Paths:** Corrected hardcoded paths in the `app.py` file to ensure the application could locate the model and other necessary files regardless of the execution directory.

## 2. Feature Enhancement: File Validation

-   **Image File Validation:** Implemented a file validation system to ensure that users can only upload image files (png, jpg, jpeg), preventing errors from non-image file uploads.
-   **Grayscale Image Check (Later Removed):** An experimental feature was added to check if an uploaded image was grayscale, as a heuristic to identify X-ray images. This was later removed to improve user experience when valid X-ray images in JPEG format were being incorrectly rejected.

## 3. Major Architectural Refactoring (and Reversion)

-   **Decoupled Frontend/Backend:** The application was refactored into a modern, decoupled architecture:
    -   **Flask REST API:** The Flask backend was converted into a REST API that returns JSON responses, with CORS enabled to allow communication with a separate frontend.
    -   **React Frontend:** A new, dynamic frontend was created using React.js, `create-react-app`, `axios` for API calls, and `antd` for a polished UI.
-   **Reversion to Server-Side Rendering:** Based on user feedback, the React frontend was removed, and the application was reverted to a server-side rendered Flask application. This demonstrated flexibility in adapting the architecture to changing requirements.

## 4. Feature Enhancement: Database-Backed User Authentication

-   **Database Integration:** The original in-memory user store (a simple dictionary) was replaced with a persistent SQLite database.
-   **SQLAlchemy ORM:** The `Flask-SQLAlchemy` extension was used to manage the database, with a `User` model to represent user data.
-   **Password Hashing:** Implemented password hashing using `werkzeug.security` to ensure that user passwords are not stored in plaintext, significantly improving security.

<h2> 5. Feature Enhancement: Full Signup and Login Flow</h2>

-   **Form-Based Authentication:** The initial Basic Auth was replaced with a more user-friendly, form-based authentication system.
-   **Session Management:** The `Flask-Login` extension was integrated to manage user sessions, including logging in, logging out, and protecting routes.
-   **Signup and Login Pages:** Created dedicated pages for user signup (`signup.html`) and login (`login.html`) with form validation and user feedback messages.

## 6. UI/UX Improvements

-   **Modern UI Redesign:** The user interface was completely redesigned with a modern, dark theme, using Bootstrap and custom CSS to create a more "fantastic" and professional look.
-   **Enhanced User Feedback:** Added more detailed health insights based on the prediction score, providing different advice for high and low pneumonia predictions.
-   **General Pneumonia Information:** A new section was added to provide users with general information about pneumonia, including its symptoms and causes.
-   **Advanced Hover Effects:** Implemented "production level" hover effects on buttons and other UI elements using advanced CSS, including transitions, transforms, and pseudo-elements, to create a more dynamic and engaging user experience.
-   **Layout and Typography:** Improved the overall layout and typography of the application, including centering the navbar title and using a new font (`Poppins`) from Google Fonts.

## 7. Bug-fixing and Robustness

-   **"Method Not Allowed" Error:** Debugged and fixed an HTTP "Method Not Allowed" error by correcting the form action in the HTML template.
-   **"Address already in use" Error:** Resolved a port conflict issue by providing clear instructions to the user and then making the `run_app.sh` script more robust.
-   **"Authentication is not opening" Issue:** Fixed an issue where the login page was not appearing by making the authentication redirect more explicit and improving the startup script.
-   **Improved Startup Script:** The `run_app.sh` script was significantly improved to:
    -   Automatically install dependencies (`pip` and `npm`).
    -   Wait for the backend to be ready before opening the browser.
    -   Automatically open the application in the user's browser.
    -   Ensure that the backend process is cleanly terminated when the script is exited.