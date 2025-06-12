pipeline {
  agent any

  environment {
    IMAGE_NAME = "aravinthexe/fastapi_app_v1"
    AWS_ECR_URI = "994390684427.dkr.ecr.eu-north-1.amazonaws.com/fastapi"
  }

  stages {
    // stage('Checkout') {
    //   steps {
    //     git branch: 'main', url: 'https://github.com/aravinth-exe/fastapi.git'

    //   }
    // }
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          docker.build("${IMAGE_NAME}")
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
          script {
            // sh """
            //   echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
            //   docker push ${IMAGE_NAME}
            // """
            bat """
              echo %DOCKER_PASSWORD% | docker login -u %DOCKER_USERNAME% --password-stdin
              docker push %IMAGE_NAME%
            """
          }
        }
      }
    }

    stage('Push to AWS ECR') {
      steps {
        // withCredentials([usernamePassword(credentialsId: 'aws-ecr', passwordVariable: 'AWS_SECRET', usernameVariable: 'AWS_ACCESS_KEY')]) {
        withCredentials([
          string(credentialsId: 'aws-access-key-id', variable: 'AWS_ACCESS_KEY_ID'),
          string(credentialsId: 'aws-secret-access-key', variable: 'AWS_SECRET_ACCESS_KEY')
        ]) {  
          script {
            bat """
              aws configure set aws_access_key_id %AWS_ACCESS_KEY_ID%
              aws configure set aws_secret_access_key %AWS_SECRET_ACCESS_KEY%
              aws ecr get-login-password --region eu-north-1 | docker login --username AWS --password-stdin 994390684427.dkr.ecr.eu-north-1.amazonaws.com
              docker tag fastapi:latest 994390684427.dkr.ecr.eu-north-1.amazonaws.com/fastapi:latest
              docker push 994390684427.dkr.ecr.eu-north-1.amazonaws.com/fastapi:latest
            """
          }
        }
      }
    }
  }
}
