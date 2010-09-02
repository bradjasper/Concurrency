cd src
git clone https://bradjasper@github.com/bradjasper/Concurrency.git
cd Concurrency/
vi requirements.txt

virtualenv env
source env/bin/activate
pip install -r requirements.txt
vi consumer.py

NUM_CONSUMERS = 10

db = redis.Redis(host="ip-10-202-222-255.ec2.internal")

