# Install

### Package requirement
   - System Packages
	1. Pillow >= 2.0.0 supports Python versions 2.6, 2.7, 3.2, 3.3, 3.4 (we use 2.7)
	2. sudo apt-get install python-dev python-setuptools
	3. sudo apt-get install libjpeg-dev (there will be an error when pip install Pillow without libjpeg)
	4. sudo aptitude install libfreetype6-dev (there will be an error when using Pillow without libfreetype6)
   - Python packages
	1. virtualenv venv
	2. source venv/bin/activate
	3. pip install -r requirements.txt
   - install MongoDb on Ubuntu LTS (14.04)
	1. sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
	2. echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
	3. sudo apt-get update
	4. sudo apt-get install -y mongodb-org

# MongoDB
### Start MongoDB
   - sudo service mongod start

### Verify that MongoDB has started successfully
Verify that the mongod process has started successfully by checking the contents of the log file at /var/log/mongodb/mongod.log for a line reading
[initandlisten] waiting for connections on port <port>
where <port> is the port configured in /etc/mongod.conf, 27017 by default.

### Stop MongoDB
   - sudo service mongod stop

### Restart MongoDB
   - sudo service mongod restart

# Execution jarvis.py
### Targets are one of those: earthquake, gas_predict, gas_price, tw_stock

### Start crawler and output to slack and txt file, for example:
  - python jarvis.py earthquake

# Unit test of Jarvis
### test packages are in folder: tests

### Start unit test, for example:
  -  py.test -s tests/test_gas_price_crawler.py -v

### test_tw_stock_crawler CI issue
  -  CI can't read the json log file which market open check saved
  -  open config.txt, modify TW_STOCK_OPEN_CHECK = off

# Deploy or git pull Jarvis
  -  open config.txt, modify TW_STOCK_OPEN_CHECK = on