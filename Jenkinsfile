pipeline{
     agent any
    
     environment {
         SCANNER_HOME=tool 'sonarqube-scanner'
         MYSQL_ROOT_PASSWORD = credentials('mysql-root-password') 
         MYSQL_DATABASE = 'FLASK_app'
     }
     
     stages {
         stage('Clean Workspace'){
             steps{
                 cleanWs()
             }
         }
         stage('Checkout from Git'){
             steps{
                 git branch: 'main', url: 'https://github.com/qkhanh39/Devops_project.git'
             }
         }
         stage("Sonarqube Analysis "){
             steps{
                 withSonarQubeEnv('sonarqube-server') {
                     sh ''' $SCANNER_HOME/bin/sonar-scanner -Dsonar.projectName=Devops-project \
                     -Dsonar.projectKey=Devops-project '''
                 }
             }
         }
         stage("Quality Gate"){
            steps {
                 script {
                     waitForQualityGate abortPipeline: false, credentialsId: 'sonarqube-token' 
                 }
             } 
         }
         stage('TRIVY FS SCAN') {
             steps {
                 sh "trivy fs . > trivyfs.txt"
             }
         }
          stage("Docker Build & Push"){
             steps{
                 script{
                    withDockerRegistry(credentialsId: 'dockerhub', toolName: 'docker'){   
                        withEnv(["MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}", "MYSQL_ROOT_PASSWORD=${MYSQL_DATABASE}"]){
                        sh "docker build -t pixel-image ."
                        sh "docker tag pixel-image qkhanh09/pixel-image:latest "
                        sh "docker push qkhanh09/pixel-image:latest "
                        }
                     }
                 }
             }
         }
         stage("TRIVY"){
             steps{
                 sh "trivy image qkhanh09/pixel-image:latest > trivyimage.txt" 
             }
         }
         stage('Deploy to Kubernetes') {
             steps {
                 script {
                     dir('K8s') {
                         withKubeConfig(credentialsId: 'kubernetes') {
                             withEnv(["DB_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}", "DB_NAME=${MYSQL_DATABASE}"]) {
                        
                        // Replace environment variables in mysql-deployment.yml
                        sh '''
                        cat mysql-deployment.yml | envsubst > mysql-deployment-final.yml
                        '''

                        sh 'kubectl delete --all pods'
                        sh 'kubectl apply -f mysql-deployment-final.yml'
                        sh 'kubectl apply -f mysql-service.yml'
                        sh 'kubectl apply -f deployment.yml'
                        sh 'kubectl apply -f service.yml'
                    }
                }
            }
        }
    }
}
     }
 }