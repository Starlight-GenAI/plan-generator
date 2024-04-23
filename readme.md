# Plan Generator service

## To start application
1. Set up environment
```sh
pip3 install virtualenv
python3 -m virtualenv env
source ./env/bin/activate
pip install --no-cache-dir --upgrade -r requirements.txt
```
2. Create config.int at root by using config.example.ini as reference
3. Update path to config in config/config.py at line 28
4. Add a Google Cloud service account in JSON format at root
5. Run
```sh
uvicorn main:app  --port=8080
```
5. The application will be running on 127.0.0.1:8080

## To start application using docker
1. Create config.int at root by using config.example.ini as reference
2. Update path to config in config/config.py at line 28
3. Add a Google Cloud service account in JSON format at root
4. Run
```sh
docker build . -t plan-generator
```
5. Run
```sh
docker run -p 8080:8080  -v ./config.ini:/<path_to_config which update at step 2> plan-generator -d
```
6. The application will be running on 127.0.0.1:8080