pipeline {
    agent any
    stages {
        stage('Lint HTML and Python files') {
            steps {
                sh '''
                tidy -q -e templates/*.html
                make install
                pylint --disable=R,C,W1203 app.py
                '''
            }
        }
        stage('Lint Docker file') {
            agent {
                docker {
                    image 'hadolint/hadolint:latest-debian'
                }
            }
            steps {
                sh 'hadolint Dockerfile'
            }
        }
        stage('Create or Update Infrastructure') {
            steps {
                script {
                    withAWS(region:'us-west-2', credentials:'udacity-devops-capstone') {
                        cfnValidate(file:'infrastructure.yml')
                        def outputs = cfnUpdate(stack:'udacity-devops-capstone', file:'infrastructure.yml', onFailure:'ROLLBACK')
                        echo("$outputs")
                    }
                }
                
            }
        }
        stage('Build and Push Docker Image') {
            agent { dockerfile true }
            stages {
                stage('Authenticate') {
                    steps {
                        sh 'aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 715480297167.dkr.ecr.us-west-2.amazonaws.com'
                    }
                }
                stage('Build') {
                    steps {
                        sh 'docker build -t udacity-devops-capstone .'
                        sh 'docker tag udacity-devops-capstone:latest 715480297167.dkr.ecr.us-west-2.amazonaws.com/udacity-devops-capstone:latest'
                    }
                }
                stage('Push') {
                    steps {
                        sh 'docker push 715480297167.dkr.ecr.us-west-2.amazonaws.com/udacity-devops-capstone:latest'
                    }
                }
            }
        }
        stage('Deploy Docker Image to EKS') {
            steps {
                withKubeConfig([credentialsId:'', serverUrl:'', clusterName:'udacity-devops-capstone-eks-cluster']) {
                    sh '''
                        kubectl run udacity-devops-capstone --image 715480297167.dkr.ecr.us-west-2.amazonaws.com/udacity-devops-capstone:latest --port 80
                        kubectl get pods --all-namespaces
                        kubectl port-forward udacity-devops-capstone 8000:80
                        kubectl logs udacity-devops-capstone
                    '''
                }
            }
        }
    }
}