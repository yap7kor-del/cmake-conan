pipeline {
    // 1. Tell Jenkins to run the entire pipeline inside a Docker compiler container
    agent {
        docker {
            image 'python:3.11-slim' // Contains Python and Pip natively
            // Pass compiler installations to the container if needed
            args '-u 0 --network jenkins-net' // Runs as root inside the container to allow installations
        }
    }

    // 2. Define your debug environment variables globally
    // environment {
    //     CONAN_LOG_LEVEL = 'debug'
    //     CMAKE_LOG_LEVEL = 'DEBUG'
    // }

    options {
        timeout(time: 10, unit: 'MINUTES')
        timestamps() // Adds timestamps to the console output for better traceability
        
        // Prevents multiple builds from running simultaneously like two pipelines run sh deploy.sh 
        disableConcurrentBuilds() 
        
        // Prevents Jenkins from doing the automatic checkout at the start
        skipDefaultCheckout() 

        buildDiscarder(
            logRotator(
                numToKeepStr: '10'  // Keeps only the last 10 builds to save space
                artifactNumToKeepStr: '5'
            )
        ) 

        skipStagesAfterUnstable() // If a stage fails or unstable, skip the remaining stages
    }


    # Define parameters for the pipeline
    # common parameters types :
    # string, booleanParam, choice, text, password
    parameters{
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
    trigger {
        // Polls the Git repository every 15 minutes for changes
        pollSCM('H/15 * * * *') 
    }

    //when is used to conditionally execute stages based on parameters or environment variables
    // allOf{} , anyOf{} , not{} used inside when{} to combine multiple conditions
    // when {
    //     expression { return params.DEPLOY == true }
    // }

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

        // stage('Verify Debug Environment') {
        //     steps {
        //         echo "=== Verification ==="
        //         // Using Jenkins environment resolution syntax
        //         echo "CONAN_LOG_LEVEL is set to: ${env.CONAN_LOG_LEVEL}"
        //         echo "CMAKE_LOG_LEVEL is set to: ${env.CMAKE_LOG_LEVEL}"
        //         echo "====================="
        //     }
        // }

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
                // Under Jenkins, we use nproc to dynamically count the CPU cores on our build node
                sh 'cmake --build build --config Release --parallel $(nproc)'
            }
        }
    }


    post {
        always {
            // Collect test results and artifacts
            //junit 'build/test-results/**/*.xml' // Collects JUnit test results
            echo "Cleaning up workspace..."
            cleanWs() // Cleans the workspace after the build, regardless of success or failure
        }
        success {
            echo "Build completed successfully!"
        }
        failure {
            echo "Build failed. Please check the logs for details."
        }
    }
}
