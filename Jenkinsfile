import hudson.AbortException

@Library('DevOps') _

pipeline {
    agent {
        label'k8s-scm-n1-s5'
    }

    
    stages { 
	
		stage('checkout') {
            steps {
                cleanWs()
                updateGitlabCommitStatus name: 'Jenkins', state: 'running'
                git branch: 'master', credentialsId: 'git_ssh', url: 'git@code.devops.fds.com:scm/ci/pricepromo-cloud-sql-capacity.git'
            }
        }
		
	      stage("Prepare Environment") {
              steps {
                  script {
					  if(!params.TierList) {
						error "TierList parameter is missing. Please make sure to fill required parameters"
						}
					  else
						{
						echo "Selected TierList = ${TierList}"
						}
				  
					  env.GOOGLE_APPLICATION_CREDENTIALS="/secrets/tfcredssecret/scm-plt-cicd-nonprod.json"
					  echo "${GOOGLE_APPLICATION_CREDENTIALS}"

                      sh '''
                      curl -sSL https://sdk.cloud.google.com  | bash -s -- --disable-prompts
                      source ~/google-cloud-sdk/path.bash.inc
                      gcloud components install beta | bash -s -- --disable-promts
                      gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                      gcloud auth list
                      gcloud config list
                      gcloud config set project mtech-commonsvc-pricepromo-np
                      '''

                  }
              }
          }



        stage("Scale Up/Down") {
            steps {
                   script {
					  sh '''
					   source ~/google-cloud-sdk/path.bash.inc
					   gcloud auth list
					   pwd
					   ls -lt
					   ls -lt ../
					   chmod +x scale_cloudsql.sh
					   sh -x scale_cloudsql.sh mtech-commonsvc-pricepromo-np:${INSTANCE} ${TierList}
					  '''
                }
        }
    }
	
  }
	
	
	
	post {
        failure {
            updateGitlabCommitStatus name: 'Jenkins', state: 'failed'
	    // dir('ci-scripts') {
        //        git branch: 'master', url: 'git@code.devops.fds.com:scm/CI/ci-scripts.git', credentialsId: 'git_ssh'
        //         sh "python notify/teams.py -r ${application} -u ${BUILD_URL}"
        //     }

        }
        unstable {
            updateGitlabCommitStatus name: 'Jenkins', state: 'failed'
        }
        success {
            updateGitlabCommitStatus name: 'Jenkins', state: 'success'
        }
        
    }
}
