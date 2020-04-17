# How to Prove My Worth
My name is Alain Sánchez Gutiérrez (https://about.me/mr.brazzi). 

I'm a Software Developer and Father, both at full time. I like self-learn and I learn quick. I enjoy teach what I learn. I believe in teamwork and help teammates when they need.

This exam was developed on Windows 10 with Python 3.6 using PyCharm 2020.1.


### 1. Steps to run as python module
#### 1.1. Create virtual environment
```shell script
virtualenv -p python .venv
```

#### 1.2. Enable virtual environment
```/bin/bash
source .venv/bin/activate
```

#### 1.3. Install requirements
```/bin/bash
pip install requirements.txt
```

#### 1.4. Run the script
```/bin/bash
python -m pyw
```
or
```/bin/bash
python pyw.py
```


### 2. Steps to build and run as Docker's container

#### Requirements
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

#### 2.1. Build custom Docker's image
````shell script
docker-compose build
````

#### 2.2. Run as Docker's container
````shell script
docker-compose run
````


### 3. Steps to build and run the flask app as Docker's container

#### Requirements
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)
* From root directory, edit the file `./pyw.py` and in line 77 add the following code:
````python
url = 'http://localhost:5000'
````

#### 3.1 Move to flask directory
````shell script
cd flask/
````

#### 3.2. Build custom Docker's image
````shell script
docker-compose build
````

#### 3.3. Run as Docker's container
````shell script
docker-compose run -d
````

#### 3.4. Check if flask app is running
Open a browser and visit the following url
````
http://localhost:5000
````
