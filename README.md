## RuachReadings

To run:

```
docker build --tag ruach-readings .

# local
docker run -p 5000:8080 ruach-readings:latest

# in AWS
docker run -d -p 5000:5000 --log-driver=awslogs --log-opt awslogs-region=us-east-1 --log-opt awslogs-group=/ruachreadings ghcr.io/shekelator/ruachreadings:main
```

### TODO
* Make sure the pipeline is running the tests
* Reduce logging level
* Set up CD to deploy automatically to new infra
* Shut down old infra
* Consider adding links to reading assistance:
    * [Tikkun here](https://swfs.org/learning/bar-bat-mitzvah/traditional-aged-bnah-mitzvah/centennial-torah-scroll/)
    * Or [Scrollscraper](https://scrollscraper.adatshalom.net/)
    * Or [here](https://www.evangel.edu/torah/)
    
