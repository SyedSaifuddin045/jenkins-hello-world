pipeline {
    agent { label 'ec2-agent' } // Replace with your agent label
    environment {
        PYTHON_FOUND_FILE = '.python_found'
        PYTHON_INSTALLED_FILE = '.python_installed'
    }
    stages {
        stage('Check Python Availability') {
            steps {
                script {
                    def status = sh(script: 'command -v python3 && python3 --version', returnStatus: true)
                    if (status == 0) {
                        echo '✓ Python3 is available'
                        writeFile file: "${env.PYTHON_FOUND_FILE}", text: 'true'
                        writeFile file: "${env.PYTHON_INSTALLED_FILE}", text: 'pre-existing'
                    } else {
                        echo '❌ Python3 is NOT available'
                        writeFile file: "${env.PYTHON_FOUND_FILE}", text: 'false'
                        writeFile file: "${env.PYTHON_INSTALLED_FILE}", text: 'none'
                    }
                }
            }
        }
        
        stage('Install Python Fallback') {
            when {
                expression {
                    return readFile(env.PYTHON_FOUND_FILE).trim() == 'false'
                }
            }
            steps {
                script {
                    echo '🔧 Attempting to install Python3...'
                    
                    // Detect OS and package manager
                    def osInfo = sh(script: '''
                        if command -v apt-get >/dev/null 2>&1; then
                            echo "debian"
                        elif command -v yum >/dev/null 2>&1; then
                            echo "rhel"
                        elif command -v dnf >/dev/null 2>&1; then
                            echo "fedora"
                        elif command -v zypper >/dev/null 2>&1; then
                            echo "suse"
                        elif command -v apk >/dev/null 2>&1; then
                            echo "alpine"
                        elif command -v brew >/dev/null 2>&1; then
                            echo "macos"
                        else
                            echo "unknown"
                        fi
                    ''', returnStdout: true).trim()
                    
                    echo "Detected OS type: ${osInfo}"
                    
                    def installStatus = 1
                    
                    switch(osInfo) {
                        case 'debian':
                            echo 'Installing Python3 on Debian/Ubuntu...'
                            installStatus = sh(script: '''
                                sudo apt-get update -qq
                                sudo apt-get install -y python3 python3-pip python3-venv
                            ''', returnStatus: true)
                            break
                            
                        case 'rhel':
                            echo 'Installing Python3 on RHEL/CentOS...'
                            installStatus = sh(script: '''
                                sudo yum update -y -q
                                sudo yum install -y python3 python3-pip
                            ''', returnStatus: true)
                            break
                            
                        case 'fedora':
                            echo 'Installing Python3 on Fedora...'
                            installStatus = sh(script: '''
                                sudo dnf update -y -q
                                sudo dnf install -y python3 python3-pip
                            ''', returnStatus: true)
                            break
                            
                        case 'suse':
                            echo 'Installing Python3 on openSUSE...'
                            installStatus = sh(script: '''
                                sudo zypper refresh
                                sudo zypper install -y python3 python3-pip
                            ''', returnStatus: true)
                            break
                            
                        case 'alpine':
                            echo 'Installing Python3 on Alpine Linux...'
                            installStatus = sh(script: '''
                                sudo apk update
                                sudo apk add python3 py3-pip
                            ''', returnStatus: true)
                            break
                            
                        case 'macos':
                            echo 'Installing Python3 on macOS...'
                            installStatus = sh(script: '''
                                brew update
                                brew install python3
                            ''', returnStatus: true)
                            break
                            
                        default:
                            echo '❌ Unknown OS or package manager. Trying generic approaches...'
                            
                            // Try to install from source as last resort
                            installStatus = sh(script: '''
                                # Try to download and compile Python from source
                                PYTHON_VERSION="3.11.7"
                                cd /tmp
                                
                                # Check if we have basic build tools
                                if ! command -v gcc >/dev/null 2>&1 && ! command -v clang >/dev/null 2>&1; then
                                    echo "❌ No C compiler found. Cannot compile Python from source."
                                    exit 1
                                fi
                                
                                # Download Python source
                                wget -q "https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz" || {
                                    echo "❌ Failed to download Python source"
                                    exit 1
                                }
                                
                                tar -xzf "Python-${PYTHON_VERSION}.tgz"
                                cd "Python-${PYTHON_VERSION}"
                                
                                # Configure and compile
                                ./configure --prefix=/usr/local --enable-optimizations --with-ensurepip=install
                                make -j$(nproc)
                                sudo make altinstall
                                
                                # Create symlinks
                                sudo ln -sf /usr/local/bin/python3.11 /usr/local/bin/python3
                                sudo ln -sf /usr/local/bin/pip3.11 /usr/local/bin/pip3
                                
                                # Update PATH for current session
                                export PATH="/usr/local/bin:$PATH"
                            ''', returnStatus: true)
                            break
                    }
                    
                    // Verify installation
                    if (installStatus == 0) {
                        def verifyStatus = sh(script: 'command -v python3 && python3 --version', returnStatus: true)
                        if (verifyStatus == 0) {
                            echo '✅ Python3 successfully installed!'
                            writeFile file: "${env.PYTHON_FOUND_FILE}", text: 'true'
                            writeFile file: "${env.PYTHON_INSTALLED_FILE}", text: 'installed'
                            
                            // Display installation info
                            sh '''
                                echo "Python3 installation details:"
                                python3 --version
                                which python3
                                python3 -c "import sys; print('Python executable:', sys.executable)"
                            '''
                        } else {
                            echo '❌ Python3 installation verification failed'
                            writeFile file: "${env.PYTHON_FOUND_FILE}", text: 'false'
                            writeFile file: "${env.PYTHON_INSTALLED_FILE}", text: 'failed'
                        }
                    } else {
                        echo '❌ Python3 installation failed'
                        writeFile file: "${env.PYTHON_FOUND_FILE}", text: 'false'
                        writeFile file: "${env.PYTHON_INSTALLED_FILE}", text: 'failed'
                    }
                }
            }
        }
        
        stage('Run Application') {
            when {
                expression {
                    return readFile(env.PYTHON_FOUND_FILE).trim() == 'true'
                }
            }
            steps {
                echo '🚀 Running Python application...'
                sh 'python3 app.py'
            }
        }
        
        stage('Testing') {
            when {
                expression {
                    return readFile(env.PYTHON_FOUND_FILE).trim() == 'true'
                }
            }
            steps {
                echo '🧪 Running Python tests...'
                sh '''
                    if [ -f "test_app.py" ]; then
                        python3 -m unittest test_app.py -v
                    else
                        echo "No test file found, running simple check..."
                        python3 -c "
import sys
import platform
print('✓ Python version:', sys.version)
print('✓ Platform:', platform.platform())
print('✓ Python executable:', sys.executable)
print('✓ Python is working correctly')

# Test basic functionality
try:
    import json, os, urllib.request
    print('✓ Standard library modules are accessible')
except ImportError as e:
    print('⚠️ Some standard library modules may not be available:', e)
"
                    fi
                '''
            }
        }
        
        stage('Fail If Python Not Available') {
            when {
                expression {
                    return readFile(env.PYTHON_FOUND_FILE).trim() == 'false'
                }
            }
            steps {
                script {
                    def installationStatus = readFile(env.PYTHON_INSTALLED_FILE).trim()
                    if (installationStatus == 'failed') {
                        error('❌ Python3 installation failed. Unable to proceed with the pipeline.')
                    } else {
                        error('❌ Python3 is not available and installation was not attempted.')
                    }
                }
            }
        }
    }
    
    post {
        success {
            script {
                def installationStatus = readFile(env.PYTHON_INSTALLED_FILE).trim()
                if (installationStatus == 'installed') {
                    echo '🎉 Pipeline completed successfully with freshly installed Python3!'
                } else {
                    echo '🎉 Pipeline completed successfully with existing Python3!'
                }
            }
        }
        failure {
            script {
                def installationStatus = readFile(env.PYTHON_INSTALLED_FILE).trim()
                echo "❌ Pipeline failed. Python installation status: ${installationStatus}"
                
                if (installationStatus == 'failed') {
                    echo '''
Troubleshooting tips:
1. Ensure the Jenkins agent has sudo privileges
2. Check internet connectivity for package downloads
3. Verify the package manager is functioning correctly
4. Consider pre-installing Python3 on the agent
5. Check Jenkins agent logs for detailed error messages
                    '''
                }
            }
        }
        always {
            script {
                // Clean up temporary files and display final status
                if (fileExists(env.PYTHON_FOUND_FILE)) {
                    def pyStatus = readFile(env.PYTHON_FOUND_FILE).trim()
                    def installStatus = readFile(env.PYTHON_INSTALLED_FILE).trim()
                    echo "📊 Final Status - Python available: ${pyStatus}, Installation: ${installStatus}"
                    
                    if (pyStatus == 'true') {
                        sh '''
                            echo "📋 Python Environment Summary:"
                            python3 --version
                            which python3
                            python3 -c "import sys; print('Site packages:', [p for p in sys.path if 'site-packages' in p][:2])"
                        '''
                    }
                } else {
                    echo '❓ Python installation status unknown.'
                }
                
                // Optional: Clean up status files
                // sh "rm -f ${env.PYTHON_FOUND_FILE} ${env.PYTHON_INSTALLED_FILE}"
            }
        }
    }
}
