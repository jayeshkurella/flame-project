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
                sh 'sudo apt-get update'
                sh 'sudo apt-get install -y python3-venv'
                sh 'sudo apt-get install -y libpq-dev' // Install PostgreSQL development libraries
                sh 'sudo apt-get install -y build-essential' // Install essential build tools
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '. venv/bin/activate && pip install -r requirements.txt || { echo "Failed to install dependencies"; exit 1; }'
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
