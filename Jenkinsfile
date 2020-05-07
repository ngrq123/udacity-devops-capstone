pipeline {
    agent any
    stages {
        stage('Lint HTML and Python files') {
            steps {
                sh '''
                tidy -q -e templates/*.html
                python3 -m venv .devops
	            . .devops/bin/activate
                python3 -m pip install --upgrade pip
	            pip3 install -r requirements.txt
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
                withAWS(region:'us-west-2', credentials:'udacity-devops-capstone') {
                    cfnValidate(file:'infrastructure.yml')
                    script {
                        cfnUpdate(stack:'udacity-devops-capstone', file:'infrastructure.yml', onFailure:'ROLLBACK', timeoutInMinutes:30)   
                    }
                }
                
            }
        }
        stage('Build and Push Docker Image') {
            steps {
                withAWS(region:'us-west-2', credentials:'udacity-devops-capstone') {
                    sh '''
                        aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 715480297167.dkr.ecr.us-west-2.amazonaws.com
                        docker build -t udacity-devops-capstone -f Dockerfile .
                        docker tag udacity-devops-capstone:latest 715480297167.dkr.ecr.us-west-2.amazonaws.com/udacity-devops-capstone:latest
                        docker push 715480297167.dkr.ecr.us-west-2.amazonaws.com/udacity-devops-capstone:latest
                    '''
                }
            }
        }
        stage('Deploy Docker Image to EKS') {
            steps {
                withAWS(region:'us-west-2', credentials:'udacity-devops-capstone') {
                // withKubeConfig([credentialsId:'udacity-devops-capstone', serverUrl:'https://4A8A7D36D2C87B13BCAB3172B9313F7E.yl4.us-west-2.eks.amazonaws.com', clusterName:'udacity-devops-capstone-eks-cluster']) {
                    sh '''
                        aws eks update-kubeconfig --name udacity-devops-capstone-eks-cluster
                        kubectl delete deployment udacity-devops-capstone --ignore-not-found=true
                        kubectl delete service currency-converter --ignore-not-found=true
                        kubectl create deployment udacity-devops-capstone --image=715480297167.dkr.ecr.us-west-2.amazonaws.com/udacity-devops-capstone:latest
                        kubectl expose deployment udacity-devops-capstone --type=LoadBalancer --port=80 --name=currency-converter
                    '''
                    script {
                        def url = kubectl get services currency-converter -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
                        echo("${url}")
                    }
                }
            }
        }
    }
}