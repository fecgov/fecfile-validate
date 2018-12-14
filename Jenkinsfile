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
       step {
          sh "kubectl --context=arn:aws:eks:us-east-1:813218302951:cluster/fecfile --namespace=dev set image deployment/fecfile-validate fecfile-validate=813218302951.dkr.ecr.us-east-1.amazonaws.com/fecfile-validate:${VERSION} --dry-run=true"
     }    
   }
  }
}
