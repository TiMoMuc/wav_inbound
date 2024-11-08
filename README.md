# THIS REPO IS UNDER DEVELOPMENT!

# Docker FastAPI App to receive .wav-files
This repository contains code to spin up a docker container. This container contains a FastAPI App which has an Endpoint to receive .wav files and stores them as blobs in an attached sqlLite Database.

## ToDo:
* [ ] Add .env file and exclude it through .gitignore
* [ ] Integrate the app directory into the container. (Not just mounted as dev version)
* [ ] Delete temporary code.

## Notes
- The env-Variable in the Dockerfile is the api-key which is needed to access the API Endpoint.

## Step by step instructions, to build the Container from source.
1. cd into the repository `cd wav_inbound`
2. We need to set an evironment variable in the Dockerfile. This is needed, to access the API.
3. We need to create a docker volume, where the database will be stored. This ensures persistency for the uploaded .wav files. 
```
docker volume create fastapi-database
```
If you need root permissions for that use:
```
sudo docker volume create fastapi-database
```
4. We can build the docker image, using the configuration in the Dockerfile and run the container.
```
docker build -t wav_receiver_api .
docker run -d -p 8801:8000 -v $(pwd)/app:/app -v fastapi-database:/data --restart=always --name wav_receiver_api wav_receiver_api
```
-> Same thing with root permissions in this case.
-> Make sure, that you run the 'docker run' command from inside the directory.

**Explanation**
- -d, running the container in detached mode.
- The port 8000 from the inside of the container is exposed on port 8801 on the outside of the container
- The /app directory is mounted as a volume so that the code can access it.
- The previously created docker volume is mounted as well under the path /data, so the code can access it also.
- restart=always, so that the container is restarted once changes are made.

## Optional
**Execute this command, to see the logs of the container**
```
docker logs -f wav_receiver_api
```
**Include this flag to remove the container once its stopped. But, this is conflicting with --restart!**
```
--rm
```

## Stuff i'm currently working with:
### 1. curl command to check the .wav endpoint
```
sudo curl -X POST "API_ENDPOINT" \
     -H "Content-Type: audio/wav" \
     -H "X-API-Key: API_KEY" \
     --data-binary "@/path/to/file.wav"
```
### 2. Temporary Docker Container to check the data on the mounted volume
```
sudo docker run --rm -it -v fastapi-database:/mnt busybox sh
```