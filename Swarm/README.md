# Running in Swarm

1. Edit the SwarmWorkers.yaml config to set number of workers (default 10)
1. Using [DeployBlueprint](https://github.com/graboskyc/DeployBlueprint), deploy the SwarmMgr.yaml config.
1. Make note of the local IP of the `manager` node
1. SSH into the `manager` node
   1. Run `sudo docker swarm init --advertise-addr <local IP>`
   2. Make note of the swarm join command and token
   3. Create the registry with `sudo docker service create --name registry --publish 5000:5000 registry:2`
1. Edit the `dockerJoinSwarm.sh` and change it to the info returned by the manager
1. Using [DeployBlueprint](https://github.com/graboskyc/DeployBlueprint), deploy the SwarmWorker.yaml 
   1. This will auto add it to the manager
2. Launch
   1. SSH into the `manager` node
   1. Edit the `docker-compose.yaml` file to add under the worker section: `deploy.mode: replicated` and `deploy.replicas: <your count>`
   1. Edit the `worker-variables.env` with the connection string, etc 
   1. Deploy the stack with `sudo docker stack deploy --compose-file ./docker-compose.yml locust`

## Troubleshooting
* Check port communication in the SG for the VPC you are using that allows docker nodes to communicate
* Check you can get to port `8089` via the SG
* Check (from the `manager`) the containers that were deployed where with `sudo docker node ps $(sudo docker node ls -q)`
* Did you edit the variables and compose files?

## Perf Tuning
* Your locust master may be working too hard. add: `deploy.resources.reservations.cpus: '48'` and `deploy.resources.reservations.memory: 8192M` or something
* Make your `users` simulated and `workers` exact multiples:
  * 19 Docker Swarm nodes? Try 190 locust workers (10x) and 38,000 users (200x)