pipeline {
    environment {
        registry = "kelseyaboy/sales_prediction_api"
        registryCredential = 'dockerhub'
        dockerImage = ''
    }
    agent any

    stages {
        stage('Cloning Git') {
            steps {
                git(
                    url: 'https://github.com/kelseyaboy/ml_eng_project.git',
                    credentialsId: 'github',
                    branch: "main"
                )
            }
        }
        stage('Install requirements') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Building image') {
            steps{
                script {
                    dockerImage = docker.build registry + ":latest"
                }
            }
        }
        stage('Deploy Image') {
            steps{
                script {
                    docker.withRegistry('', registryCredential) {
                        dockerImage.push()
                    }
                }
            }
        }
        stage('Remove Unused docker image') {
            steps{
                sh "docker rmi $registry" + ":latest"
            }
        }
        stage('Push image to Heroku') {
            steps{
                sh "heroku git:remote -a ka-sales-prediction-app"
                sh "heroku container:push web"
            }
        }
        stage('Release image in Heroku') {
            steps{
                sh "heroku container:release web"
            }
        }
    }
}