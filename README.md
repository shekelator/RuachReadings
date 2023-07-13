## RuachReadings

To run:

```
docker build --tag ruach-readings .

# local
docker run -p 5000:5000 ruach-readings:latest

# in AWS
docker run -d -p 5000:5000 --log-driver=awslogs --log-opt awslogs-region=us-east-1 --log-opt awslogs-group=/ruachreadings ruach-readings:latest
```

### TODO
* Make sure the pipeline is running the tests
* Reduce logging level
* Set up CD to deploy automatically to new infra
* Shut down old infra
