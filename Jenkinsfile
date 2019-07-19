pipeline {
  agent any
  stages {
    stage('Prepare Build') {
      steps {
        script {
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
        deployImage("${VERSION}", "dev")
        code_quality("${BUILD_ID}", "${VERSION}") 
      }
    }
    stage('Deploy to QA '){
      when { branch "release"}
      steps {
        deployImage("${VERSION}", "qa")
      }
    }
    stage('Deploy to UAT '){
      when { branch "master"}
      steps {
        deployImage("${VERSION}", "uat")
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

def deployImage(String version, String toEnv) {
   sh """
    kubectl \
      --context=arn:aws:eks:us-east-1:813218302951:cluster/fecfile \
      --namespace=${toEnv} \
      set image deployment/fecfile-validate \
      fecfile-validate=813218302951.dkr.ecr.us-east-1.amazonaws.com/fecfile-validate:${version}
   """
   if ( toEnv == "dev" || toEnv == "qa" ){
     sh """
       kubectl \
         --context=arn:aws:eks:us-east-1:813218302951:cluster/fecfile4 \
         --namespace=${toEnv} \
         set image deployment/fecfile-validate \
         fecfile-validate=813218302951.dkr.ecr.us-east-1.amazonaws.com/fecfile-validate:${version}
   """
   }
}

def code_quality(String id, String hash) {
  sh """
    sh successful_test.sh "${id}" ${hash}
  """
  junit '**/reports/*.xml'
}
