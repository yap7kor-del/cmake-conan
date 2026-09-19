pipeline {
    // 1. Run the entire pipeline inside a clean Docker compiler container
    agent {
        docker {
            image 'python:3.11-slim' // Contains Python and Pip natively
            // FIX: Changed network name to 'jenkins-net' to match our newly created bridge network
            args '-u 0' 
        }
    }
    stages {
        stage('Install System Compilers') {
            steps {
                echo "Installing GCC, G++, and CMake inside the container..."
                sh '''
                    apt-get update && apt-get install -y \
                        build-essential \
                        cmake \
                        git
                '''
            }
        }

        stage('Install Conan') {
            steps {
                echo "Installing Conan Package Manager..."
                sh 'pip install conan'
            }
        }

        stage('Detect Conan Profile') {
            steps {
                echo "Detecting compiler profiles..."
                sh 'conan profile detect'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing packages with Conan..."
                sh '''
                    conan install . \
                        --output-folder=build \
                        --build=missing \
                        -s build_type=Release
                '''
            }
        }

        stage('Configure CMake') {
            steps {
                echo "Generating build configuration using Conan presets..."
                sh 'cmake --preset conan-release'
            }
        }

        stage('Build') {
            steps {
                echo "Compiling project binaries..."
                sh 'cmake --build build --config Release --parallel $(nproc)'
            }
        }
    }

    post {
        always {
            echo "Cleaning up workspace..."
            cleanWs() // Clear files to keep laptop storage completely clean [source: 21]
        }
        success {
            echo "Build completed successfully!"
        }
        failure {
            echo "Build failed. Please check the logs for details."
        }
    }
}
