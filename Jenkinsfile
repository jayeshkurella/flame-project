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
                echo "Setting up the Python environment"
                // Update the package list and install python3-venv
                //sh 'sudo apt-get update && sudo apt-get install -y python3-venv'
                // Create a virtual environment
                sh 'python3 -m venv ${VIRTUALENV_PATH}'
                // Activate the virtual environment and install dependencies
                sh """
                    . ${VIRTUALENV_PATH}/bin/activate
                    pip install --upgrade pip
                    pip install -r ${REQUIREMENTS_FILE}
                """
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
                sh '. venv/bin/activate && python flames/manage.py migrate'
           }
        }

        stage('Run Tests') {
            steps {
                // Run Django tests
                sh '. venv/bin/activate && python flames/manage.py test'
            }
        }

        stage('Deploy') {
            steps {
                // Add deployment steps here
                // For example, copying files to the server, restarting services, etc.
                sh '. venv/bin/activate && python flames/manage.py runserver 0.0.0.0:9000'
                // Add other deployment steps specific to your environment
            }
        }
    }
}
