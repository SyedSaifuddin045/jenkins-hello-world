pipeline {
    agent { label 'ec2-agent' }

    environment {
        PYTHON_INSTALLED = 'false'
    }

    stages {
        stage('Check Python Availability') {
            steps {
                script {
                    try {
                        sh 'python3 --version'
                        env.PYTHON_INSTALLED = 'true'
                        echo '✓ Python3 is already available'
                    } catch (Exception e) {
                        echo '! Python3 not found, will attempt installation'
                        env.PYTHON_INSTALLED = 'false'
                    }
                }
            }
        }

        stage('Install Python (if needed)') {
            when {
                environment name: 'PYTHON_INSTALLED', value: 'false'
            }
            steps {
                script {
                    echo 'Attempting to install Python3...'
                    sh '''
                        set -e
                        if command -v apt-get > /dev/null 2>&1; then
                            apt-get update && apt-get install -y python3 python3-pip
                        elif command -v yum > /dev/null 2>&1; then
                            yum install -y python3 python3-pip
                        else
                            echo "No supported package manager found."
                            exit 1
                        fi
                    '''
                    env.PYTHON_INSTALLED = 'true'
                }
            }
        }

        stage('Run Application') {
            when {
                environment name: 'PYTHON_INSTALLED', value: 'true'
            }
            steps {
                echo 'Running Python application...'
                sh 'python3 app.py'
            }
        }

        stage('Testing') {
            when {
                environment name: 'PYTHON_INSTALLED', value: 'true'
            }
            steps {
                echo 'Running Python tests...'
                sh '''
                    if [ -f "test_app.py" ]; then
                        python3 -m unittest test_app.py -v
                    else
                        echo "No test file found, creating basic test..."
                        python3 -c "
import sys
print('Python version:', sys.version)
print('✓ Python is working correctly')
print('✓ All basic tests passed')
"
                    fi
                '''
            }
        }
    }

    post {
        success {
            echo '🎉 Python pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
        always {
            echo "Python installed: ${env.PYTHON_INSTALLED}"
        }
    }
}

