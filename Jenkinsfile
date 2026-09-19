pipeline {
    // 1. Run the entire pipeline inside a clean Docker compiler container
    agent {
        docker {
            image 'python:3.11-slim' // Contains Python and Pip natively
            // FIX: Changed network name to 'jenkins-net' to match our newly created bridge network
            args '-u 0' 
        }
    }

    options {
        timeout(time: 10, unit: 'MINUTES') // Prevents hanging builds
        timestamps() // Adds timestamps to the console logs
        disableConcurrentBuilds() // Prevents overlapping concurrent runs
        skipDefaultCheckout() // Overrides default checkout so we can manually manage workspace if needed
        
        buildDiscarder(
            logRotator(
                numToKeepStr: '10',  // Retain logs of only the last 10 builds
                artifactNumToKeepStr: '5'
            )
        ) 
        skipStagesAfterUnstable() // Skip downstream stages if preceding checks fail
    }

    //  FIX: Changed comments from Python '#' to Groovy '//'
    // Define parameters for the pipeline
    parameters {
        string(
            name: 'CONAN_LOG_LEVEL', 
            defaultValue: 'debug', 
            description: 'Set Conan log level'
        )
        booleanParam(
            name: 'DEPLOY', 
            defaultValue: false, 
            description: 'Enable deployment after build'
        )
        choice(
            name: 'BUILD_TYPE', 
            choices: ['Debug', 'Release'], 
            description: 'Select the build type'
        )
    }

    //   FIX: Changed singular 'trigger' to plural 'triggers'
    triggers {
        // Polls the Git repository every 15 minutes for changes [source: 15]
        pollSCM('H/1 * * * *') 
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
