pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/madhav8511/BrainTumor-SPE.git'
            }
        }

        stage('Setup Python venv') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate && pip install --upgrade pip
                    . venv/bin/activate && pip install -r requirements.txt
                '''
            }
        }

        stage('DVC Pull') {
            steps {
                sh '''
                    . venv/bin/activate && dvc pull
                '''
            }
        }

        stage('Reproduce DVC Pipeline') {
            steps {
                sh '''
                    . venv/bin/activate && dvc repro
                '''
            }
        }

        stage('DVC Push') {
            steps {
                sh '''
                    . venv/bin/activate && dvc push
                '''
            }
        }

        stage('Promote Model to Production') {
            steps {
                sh '''
                    . venv/bin/activate && python src/promote_model.py
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
         always {
            sh '''
            sudo chown -R madhav /home/madhav/Desktop/BrainTumor-SPE/mlruns
            sudo chgrp -R mlops /home/madhav/Desktop/BrainTumor-SPE/mlruns
            '''
        }
    }
}