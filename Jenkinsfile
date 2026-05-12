pipeline {
    agent any

    environment {
        DOCKERHUB_USER  = credentials('dockerhub-username')
        DOCKERHUB_TOKEN = credentials('dockerhub-token')
        IMAGE_NAME      = "fastapi-playwright-demo"
        IMAGE_TAG       = "latest"
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Backend tests (pytest)') {
            agent {
                docker {
                    image 'python:3.11-slim'
                    args '-u'
                }
            }
            steps {
                sh '''
                  pip install -r requirements.txt
                  pytest -q
                '''
            }
        }

        stage('Build & Push Docker image') {
            steps {
                sh "echo ${DOCKERHUB_TOKEN} | docker login -u ${DOCKERHUB_USER} --password-stdin"
                sh """
                  docker build -t ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} .
                  docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('UI tests (Playwright)') {
            agent {
                docker {
                    image 'mcr.microsoft.com/playwright:v1.49.0-jammy'
                    args '--network host'
                }
            }
            steps {
                script {
                    sh """
                      docker run -d --rm \
                        --name fastapi-app-ci \
                        -p 8000:8000 \
                        ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}
                    """

                    sh '''
                      for i in {1..20}; do
                        if curl -fsS http://localhost:8000/api/health > /dev/null; then break; fi
                        sleep 3
                      done
                    '''

                    sh '''
                      npm install
                      npx playwright install --with-deps
                      BASE_URL=http://localhost:8000 npx playwright test
                    '''
                }
            }
            post { always { sh 'docker stop fastapi-app-ci || true' } }
        }
    }

    post { always { cleanWs() } }
}
