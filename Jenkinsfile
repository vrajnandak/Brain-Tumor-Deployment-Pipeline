pipeline {
    agent any

    environment {
        PYENV = ".venv"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'automate', url: 'https://github.com/madhav8511/BrainTumor-SPE.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                echo "Creating virtual environment..."
                python3 -m venv ${PYENV}
                source ${PYENV}/bin/activate

                echo "Upgrading pip..."
                pip install --upgrade pip
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                source ${PYENV}/bin/activate
                echo "Installing project dependencies..."
                pip install -r requirements.txt
                '''
            }
        }

        stage('DVC Pull') {
            steps {
                sh '''
                source ${PYENV}/bin/activate
                echo "Pulling dataset from DVC remote..."
                dvc pull
                '''
            }
        }

        stage('Reproduce Pipeline') {
            steps {
                sh '''
                source ${PYENV}/bin/activate
                echo "Running DVC pipeline..."
                dvc repro
                '''
            }
        }

        stage('DVC Push') {
            steps {
                sh '''
                source ${PYENV}/bin/activate
                echo "Pushing updated artifacts to DVC remote..."
                dvc push
                '''
            }
        }

        stage('Promote Model to Production') {
            steps {
                sh '''
                source .venv/bin/activate
                echo "Promoting latest model to Production..."
                python src/promote_model.py
                '''
            }
        }
    }

    post {
        success {
            echo "🎉 Pipeline Completed Successfully!"
        }
        failure {
            echo "❌ Pipeline Failed. Please check logs."
        }
    }
}
