pipeline {
    agent any

    stages {
        stage('auto test') {
            steps {
                sh 'python3 debug.py'
            }
        }
    }
    post {
      success {
      	// 注意报告地址写相对路径，也就是--alluredir后面的路径,如我的报告路径：report/allure_raw，但不要写成 /report/allure_raw
        allure includeProperties: false, jdk: 'jdk1.8', results: [[path: 'report/allure_raw']]
      }
    }
}
