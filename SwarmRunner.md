# Running in Swarm

1. Edit the Swarm.yaml config to set number of workers
1. Using DeployBlueprint, deploy the Swarm.yaml config.
1. Make note of the local IP of the `manager` node
1. SSH into the `manager` node
   1. Run `sudo docker swarm init --advertise-addr <local IP>`
   2. Make note of the swarm join command and token
   3. Install `docker-compose`
   4. Create the registry with `sudo docker service create --name registry --publish 5000:5000 registry:2`
2. For each worker node:
   1. SSH in to each
   2. Run the `swarm join` command shown by the `manager`
3. Launch
   1. clone this repo onto the `manager`
   2. prep the images by running the `build.sh` script
   3. test it is running ok with `sudo docker-compose up`  
   4. Visit the web page `http://<managerHostName>:8089` to make sure it works
   5. and then press `control+c` to kill it
   6. push to the registry you made earlier by running `docker-compose push`
   7. Edit the `docker-compose.yaml` file to add under the worker section: `deploy.mode: replicated` and `deploy.replicas: <your count>`
   8. Deploy the stack with `docker stack deploy --compose-file ./docker-compose.yml locust`
4. Troubleshooting