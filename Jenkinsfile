pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
            }
        }

        stage('Verify Docker') {
            steps {
                sh 'docker --version'
                sh 'docker ps'
            }
        }

        stage('Verify Repo Structure') {
            steps {
                sh 'ls -la'
                sh 'ls -la training'
                sh 'ls -la api'
                sh 'ls -la trigger'
            }
        }
    }
}
