pipeline {

    agent any

    stages {

        stage('Clean Workspace') {
            steps {
                sh 'rm -rf student-management'
            }
        }

        stage('Deploy to EC2') {
            steps {
                sh '''
                    ssh -o StrictHostKeyChecking=no -i /var/lib/jenkins/student-management.pem admin@13.200.222.165 << EOF

                    cd ~

                    rm -rf student-management

                    if [ -d "student-management" ]; then
                        cd student-management
                    else
                        git clone -b Jenkins https://github.com/prathameshkarve01/student-management.git
                        cd student-management
                    fi

                    python3 -m venv venv

                    ./venv/bin/pip install --upgrade pip

                    ./venv/bin/pip install -r requirements.txt

                    ./venv/bin/python seed_admin.py

                    sudo apt install lsof -y

                    PID=$(lsof -t -i:8000)
                    
                    if [ -n "$PID" ]; then
                        kill -9 $PID
                    fi

                    nohup ./venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &

EOF
                '''
            }
        }
    }
}