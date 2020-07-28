pipeline {
    agent none
    stages {
        stage('Build') {
            agent {
                node {
                    label 'master'
                }
            }
            steps {
                script {
                    docker.build("mlb-fantasy-lifetime")
                }
            }
        }
    }
}