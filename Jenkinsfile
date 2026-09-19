pipeline {

    agent {
        docker {
            image 'python:3.11-slim'
            args '-u 0'
        }
    }

    options {
        timeout(time: 20, unit: 'MINUTES')
        timestamps()
        disableConcurrentBuilds()

        buildDiscarder(
            logRotator(
                numToKeepStr: '10',
                artifactNumToKeepStr: '5'
            )
        )
    }

    parameters {
        choice(
            name: 'BUILD_TYPE',
            choices: ['Debug', 'Release'],
            description: 'Select build type'
        )

        booleanParam(
            name: 'DEPLOY',
            defaultValue: false,
            description: 'Deploy after build'
        )
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Debug Environment') {
            steps {
                sh '''
                    whoami
                    pwd
                    ls -la
                    cat /etc/os-release
                    python --version
                '''
            }
        }

        stage('Install Build Tools') {
            steps {
                echo 'Installing GCC, CMake and Git...'

                sh '''
                    apt-get update

                    apt-get install -y \
                        build-essential \
                        cmake \
                        git

                    gcc --version
                    cmake --version
                    git --version
                '''
            }
        }

        stage('Install Conan') {
            steps {
                echo 'Installing Conan...'

                sh '''
                    pip install --no-cache-dir conan==2.21.0
                    conan --version
                '''
            }
        }

        stage('Detect Conan Profile') {
            steps {
                sh '''
                    conan profile detect --force
                    conan profile show
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh """
                    conan install . \
                        --output-folder=build \
                        --build=missing \
                        -s build_type=${params.BUILD_TYPE}
                """
            }
        }

        stage('Configure CMake') {
            steps {
                sh """
                    cmake --preset conan-${params.BUILD_TYPE.toLowerCase()}
                """
            }
        }

        stage('Build') {
            steps {
                sh """
                    cmake --build build \
                        --config ${params.BUILD_TYPE} \
                        --parallel
                """
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts(
                    artifacts: 'build/**/*',
                    fingerprint: true,
                    allowEmptyArchive: true
                )
            }
        }
    }

    post {

        always {
            cleanWs(
                deleteDirs: true,
                notFailBuild: true
            )
        }

        success {
            echo '✅ Build completed successfully.'
        }

        failure {
            echo '❌ Build failed. Check console output.'
        }
    }
}