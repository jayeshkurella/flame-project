pipeline {
    agent any

    environment {
        DJANGO_SETTINGS_MODULE = 'flames.settings'
        PYTHON_ENV = 'production'
        VIRTUALENV_PATH = 'venv'
        REQUIREMENTS_FILE = 'requirements.txt'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/jayeshkurella/flame-project.git'
            }
        }

        stage('Set up Python Environment') {
            steps {
                sh '''
                sudo apt-get update
                sudo apt-get install -y python3-venv
                sudo apt-get install -y libpq-dev
                sudo apt-get install -y build-essential
                python3 -m venv ${VIRTUALENV_PATH}
                . ${VIRTUALENV_PATH}/bin/activate && pip install --upgrade pip
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                . ${VIRTUALENV_PATH}/bin/activate
                pip install -r ${REQUIREMENTS_FILE} || { echo "Failed to install dependencies"; exit 1; }
                pip list
                '''
            }
        }

        stage('Verify Dependencies') {
            steps {
                sh '''
                . ${VIRTUALENV_PATH}/bin/activate
                pip show django-environ
                pip show django-cors-headers
                '''
            }
        }

        stage('Run Migrations') {
            steps {
                sh '''
                . ${VIRTUALENV_PATH}/bin/activate
                python flames/manage.py migrate
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . ${VIRTUALENV_PATH}/bin/activate
                python flames/manage.py test
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                . ${VIRTUALENV_PATH}/bin/activate
                python flames/manage.py runserver 0.0.0.0:9000
                '''
            }
        }
    }
}
