pipeline {
    agent any

    parameters {
        string(name: 'BASE_URL', defaultValue: 'https://claroty.com', description: 'Target Claroty base URL')
        choice(name: 'BROWSER', choices: ['chromium', 'firefox', 'webkit'], description: 'Playwright browser')
        string(name: 'TEST_MARKER', defaultValue: 'smoke', description: 'pytest marker expression')
        booleanParam(name: 'HEADLESS', defaultValue: true, description: 'Run browser headless')
    }

    environment {
        BASE_URL = "${params.BASE_URL}"
        BROWSER = "${params.BROWSER}"
        HEADLESS = "${params.HEADLESS}"
        PIP_DISABLE_PIP_VERSION_CHECK = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create Python virtual environment') {
            steps {
                sh 'python3 -m venv .venv'
            }
        }

        stage('Install Python dependencies') {
            steps {
                sh '.venv/bin/python -m pip install --upgrade pip setuptools wheel'
                sh '.venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Install Playwright Chromium and required system dependencies') {
            steps {
                sh '.venv/bin/python -m playwright install --with-deps chromium'
                sh '''
                    if [ "${BROWSER}" != "chromium" ]; then
                        .venv/bin/python -m playwright install "${BROWSER}"
                    fi
                '''
            }
        }

        stage('Run pytest') {
            steps {
                sh '''
                    rm -rf allure-results artifacts
                    mkdir -p allure-results artifacts
                    .venv/bin/pytest -m "${TEST_MARKER}" \
                        --browser "${BROWSER}" \
                        --headless "${HEADLESS}" \
                        --alluredir=allure-results \
                        --clean-alluredir \
                        --junitxml=artifacts/junit.xml
                '''
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'artifacts/junit.xml'
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            archiveArtifacts allowEmptyArchive: true, artifacts: 'artifacts/**/*.png, artifacts/**/*.zip, artifacts/**/*.html, artifacts/**/*.log, artifacts/junit.xml'
        }
    }
}
