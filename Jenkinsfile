pipeline {
    agent any

    stages {
        stage('checkout code') {
            steps {
                sh "pwd"
                //checkout([$class: 'GitSCM', branches: [[name: '*/分支']], extensions: [], userRemoteConfigs: [[credentialsId: '秘钥id', url: '你的仓库地址']]])
                checkout(
                    [
                        $class: 'GitSCM', 
                        branches: [[name: '*/master']], 
                        extensions: [
                            [$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: true, recursiveSubmodules: true, reference: '', trackingSubmodules: false],
                            [$class: 'CloneOption', shallow: false, noTags: false, reference: '', timeout: null, depth: 0, honorRefspec: false]
                        ],
                        userRemoteConfigs: [[credentialsId: 'zh', url: 'git@github.com:dino666666/tmp.git']]
                    ]
                )
            }
        }
        stage('auto test') {
            steps {
                sh 'pwd'
                sh 'python3 debug.py'
            }
        }
    }
    post {
      success {
      	// 注意报告地址写相对路径，也就是--alluredir后面的路径,如我的报告路径：report/allure_raw，但不要写成 /report/allure_raw
        allure includeProperties: false, jdk: 'jdk11', results: [[path: 'report/allure_raw']]
      }
    }
}
