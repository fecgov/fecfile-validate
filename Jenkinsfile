pipeline {

  agent any

  stages {

    stage('Prepare Build') {
      steps {
                script
                {
                    hash = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
                    VERSION = hash.take(7)
                    currentBuild.displayName = "#${BUILD_ID}-${VERSION}"

                    sh("eval \$(aws ecr --region us-east-1 get-login --no-include-email)")
                }
            }
    }

    stage('Build DataReceiver') {
      steps {
        script {
          def validateImage = docker.build("fecfile-validate:${VERSION}", '. -f Dockerfile-run')

          docker.withRegistry('https://813218302951.dkr.ecr.us-east-1.amazonaws.com/fecfile-validate') {
            validateImage.push()
          }

        }
      }

    }
   stage('Deploy to dev '){
       when { branch "develop"}
       steps {
          sh "kubectl --context=arn:aws:eks:us-east-1:813218302951:cluster/fecfile --namespace=dev set image deployment/fecfile-validate fecfile-validate=813218302951.dkr.ecr.us-east-1.amazonaws.com/fecfile-validate:${VERSION}"
     }
   }
   stage('Deploy to QA '){
       when { branch "release"}
       steps {
          sh "kubectl --context=arn:aws:eks:us-east-1:813218302951:cluster/fecfile --namespace=qa set image deployment/fecfile-validate fecfile-validate=813218302951.dkr.ecr.us-east-1.amazonaws.com/fecfile-validate:${VERSION}"
     }
   }
   stage('Deploy to UAT '){
       when { branch "master"}
       steps {
          sh "kubectl --context=arn:aws:eks:us-east-1:813218302951:cluster/fecfile --namespace=uat set image deployment/fecfile-validate fecfile-validate=813218302951.dkr.ecr.us-east-1.amazonaws.com/fecfile-validate:${VERSION}"
     }
   }
 }
   post{
     success {
       slackSend color: 'good', message: env.BRANCH_NAME + ": Deployed ${VERSION} of fecfile-Validate to k8s"
     }
     failure {
       slackSend color: 'danger', message: env.BRANCH_NAME + ": Deployment of ${VERSION} failed"
     }
   }

}
