pipeline {
    agent any

    environment {
        PROJECT_ID = 'project-b346305c-6a86-4392-9d4'
        REGION = 'us-central1'
        REPOSITORY = 'fraud-repo'
        API_SERVICE = 'fraud-api'
        API_IMAGE = "us-central1-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/fraud-api:${BUILD_NUMBER}"
    }

    stages {
        stage('Authenticate GCP') {
            steps {
                sh '''
                    gcloud config set project $PROJECT_ID
                    gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet
                '''
            }
        }

        stage('Build API Image') {
            steps {
                sh '''
                     docker system prune -af || true
                      docker build  --no-cache --platform linux/amd64 -t $API_IMAGE ./api'''
            }
        }

        stage('Push API Image') {
            steps {
                sh 'docker push $API_IMAGE'
            }
        }

        stage('Deploy API to Cloud Run') {
            steps {
                sh '''
                    gcloud run deploy $API_SERVICE \
                      --image $API_IMAGE \
                      --region $REGION \
                      --platform managed \
                      --allow-unauthenticated
                '''
            }
        }
    }
}
