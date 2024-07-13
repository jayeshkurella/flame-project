pipeline {
    agent any

    environment {
        // Add any necessary environment variables here
        PYTHON_ENV = 'production'
        VIRTUALENV_PATH = 'venv'
        REQUIREMENTS_FILE = 'requirements.txt'
    }

    stages {
        stage('Checkout') {
            steps {
                // Clone the repository
                git 'https://github.com/jayeshkurella/flame-project.git'
            }
        }

        stage('Set up Python Environment') {
            steps {
                // Set up a Python virtual environment
                sh ' sudo apt python3 -m venv venv'
                sh '. venv/bin/activate'
            }
        }

        stage('Install Dependencies') {
            steps {
                // Install the project dependencies
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Migrations') {
            steps {
                // Run Django migrations
                sh '. venv/bin/activate && python flame/manage.py migrate'
            }
        }

        stage('Run Tests') {
            steps {
                // Run Django tests
                sh '. venv/bin/activate && python flame/manage.py test'
            }
        }

        stage('Deploy') {
            steps {
                // Add deployment steps here
                // For example, copying files to the server, restarting services, etc.
                sh '. venv/bin/activate && python flame/manage.py collectstatic --noinput'
                // Add other deployment steps specific to your environment
            }
        }
    }
}
