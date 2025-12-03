pipeline {

    agent any

    environment {
        DOCKER_IMAGE = "madhavgirdhar/braintumor"
        VAULT_CREDS = "ansible-vault-pass"
    }

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

        stage('Fetch Latest Model From MLflow') {
            steps {
                sh """
                echo "Fetching latest model from MLflow Registry..."

                . venv/bin/activate && python backend/save_model.py
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                echo "Building Docker image..."

                docker build \
                    --build-arg MODEL_VERSION=\$(date +%s) \
                    -t $DOCKER_IMAGE:$BUILD_NUMBER backend/
                """
            }
        }

        stage("Push to Docker Hub"){
            steps{
                echo "Pushing Image to Hub..."
                script{
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                        docker.image("${DOCKER_IMAGE}:${BUILD_NUMBER}").push()
                    }
                }
            }
        }

        stage('Deploy On k8 using Ansible') {
            steps {
                withCredentials([string(
                    credentialsId: "${VAULT_CREDS}",
                    variable: "VAULT_PASS"
                )]) {
                    sh """
                        echo "$VAULT_PASS" > .vault_pass

                        ansible-playbook playbook.yaml \
                        -i inventory.ini \
                        --vault-password-file .vault_pass \
                        --extra-vars "build_number=${BUILD_NUMBER}"

                        rm -f .vault_pass
                    """
                }
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
            sudo chmod -R 770 /home/madhav/Desktop/BrainTumor-SPE/mlruns
            '''
        }
    }
}