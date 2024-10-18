pipeline {
    agent any

    stages {

        stage("build") {

            steps {
                echo "This is the build stage"
            }
        }

        stage("test") {

            steps {
                echo "This is the test stage"
            }
        }

        stage("deploy") {

            steps {
                echo "This is the deploy stage"
                echo "The pipeline has finished!"
            }
        }
    }
}