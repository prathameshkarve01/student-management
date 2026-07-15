pipeline {

    agent any

    stages {

        stage('Deploy') {

            steps {

                sshagent(credentials: ['ec2-key']) {

                    sh '''

                    ssh -o StrictHostKeyChecking=no admin@13.235.80.61 << EOF

                    cd ~

                    rm -rf student-management

                    git clone -b Jenkins https://github.com/prathameshkarve01/student-management.git

                    cd student-management

                    python3 -m venv venv

                    ./venv/bin/pip install --upgrade pip

                    ./venv/bin/pip install -r requirements.txt

                    ./venv/bin/python seed_admin.py

                    sudo apt install -y lsof

                    kill \$(lsof -t -i:8000) || true

                    nohup ./venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &

                    EOF

                    '''

                }

            }

        }

    }

}