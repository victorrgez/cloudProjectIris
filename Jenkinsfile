pipeline {
    agent any

    stages {

        stage("build") {

            steps {
                echo "This is the first human step of the pipeline (Check out stage is done automatically!)"
                echo "This is the build stage"
            }
        }

        stage("test") {

            steps {
                echo "This is the test stage"
                script {
                    def test = 2 + 2 > 3 ? 'cool' : 'not cool'
                    echo test
                }
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