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

        stage('Install Missing Packages') {
            steps {
                sh '''
                . ${VIRTUALENV_PATH}/bin/activate
                pip show django-cors-headers || pip install django-cors-headers
                pip show django-sslserver || pip install django-sslserver
                pip show shapely || pip install shapely
                pip show pystac || pip install pystac
                pip show rasterio || pip install rasterio
                '''
            }
        }

        stage('Verify Dependencies') {
            steps {
                sh '''
                . ${VIRTUALENV_PATH}/bin/activate
                pip show django-environ
                pip show django-cors-headers
                pip show django-sslserver
                pip show shapely
                pip show pystac
                pip show rasterio
                '''
            }
        }

        stage('Run Migrations') {
            steps {
                sh '''
                . ${VIRTUALENV_PATH}/bin/activate
                python3 flames/manage.py migrate
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . ${VIRTUALENV_PATH}/bin/activate
                python3 flames/manage.py test
                '''
            }
        }

         stage('Deploy') {
            steps {
                sh '''
                . ${VIRTUALENV_PATH}/bin/activate
                python3 flames/manage.py runserver 0.0.0.0:9000
                '''
            }
        }
    }
}

post {
        always {
            // Clean up the workspace
            cleanWs()
        }
        success {
            // Notify success
            echo 'Deployment succeeded!'
        }
        failure {
            // Notify failure
            echo 'Deployment failed!'
        }
}
