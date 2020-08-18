_GitHub URL: https://github.com/ngrq123/udacity-devops-capstone_

# Udacity Cloud DevOps Engineer Nanodegree Capstone

A currency converter application built with the Python Flask framework and dockerised into a Docker container that is pushed to AWS Elastic Container Registry (ECR). The container is then pulled and deployed by nodes in an AWS Elastic Kubernetes Service (EKS) cluster.

The Kubernetes cluster is deployed in the Jenkins pipeline with an AWS CloudFormation script `infrastructure.yml` in two Availability Zones (AZs), with a node group comprising of at least two EC2 instances in each AZ.

A Jenkins pipeline runs in an AWS Elastic Cloud Compute (EC2) instance running on Ubuntu 18.04. Rolling deployment is used using the following pipeline steps in `Jenkinsfile`:
* Lint HTML and Python files
* Lint Docker files
* Create ECR, build and push Docker image
* Create or update infrastructure
* Deploy Docker image to EKS

# The Application: Currency Converter

A Python flask app that calculates whether withdrawing an amount in a target currency is possible with a balances in a multi-currency wallet, purely based on current exchange rates (i.e. no charges of any form).

Currently, it supports 3 currencies: USD, EUR and GBP. The order of withdrawal begins with the withdrawal (target) currency, followed by USD, EUR, then GBP.

This application utilises [Exchange Rates API](https://exchangeratesapi.io) to retrieve live exchange rates.

## Example Usage
Suppose you have 100 USD, 70 EUR and 50 GBP, and would like to withdraw 150 GBP from your wallet. 

Assuming the exchange rates (retrieved from the API) are:
* 1 GBP = 1.2454628992 USD
* 1 GBP = 1.1486331266 EUR


It will be possible to withdraw all 50 GBP from your wallet, convert 80.29 GBP from 100 USD, and convert 19.71 GBP from 22.64 EUR. This leaves 47.36 EUR in your wallet.

# Environment Setup

1. Create an AWS EC2 instance with Ubuntu 18.04 x86 AMI
2. Install [Jenkins](https://www.jenkins.io/doc/book/installing/#debianubuntu) and the following plugins
     * BlueOcean
     * CloudBees AWS Credentials
     * Pipeline: AWS Steps
3. Install [tidy](https://askubuntu.com/a/823272), [pip](https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/), [python3-venv](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-ubuntu-18-04-quickstart), [Docker](https://docs.docker.com/engine/install/ubuntu/), [awscli](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) and [kuberctl](https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html)
     * Add Jenkins to docker group `sudo usermod -a -G docker jenkins` ([Reference](https://stackoverflow.com/a/48450294))
     * Install `kubectl` in global `bin` file for Jenkins to access
     * Restart Jenkins `sudo systemctl restart jenkins`
4. Setup AWS credentials on Jenkins
5. Setup Pipeline on Jenkins BlueOcean UI
6. Login to AWS using `aws configure`

# Accessing the Load Balancer Endpoint

1. With the same AWS IAM user logged in, update the Kubernetes configuration file: `aws eks update-kubeconfig --name udacity-devops-capstone-eks-cluster`
2. Retrieve the Load Balancer DNS: `kubectl get services currency-converter`
      * The link ends with `us-west-2.elb.amazonaws.com`

# Deleting Resources
1. Delete load balancer
2. Delete CloudFormation stack
3. Delete ECR