## RuachReadings

To run:

```
docker build --tag ruach-readings .

# local
docker run -p 5000:8080 ruach-readings:latest

# in AWS
docker run -d -p 5000:5000 --log-driver=awslogs --log-opt awslogs-region=us-east-1 --log-opt awslogs-group=/ruachreadings ghcr.io/shekelator/ruachreadings:main
```

### Troubleshooting Docker Local Run

If you run `docker run -p 5000:8080 ruach-readings:latest`, the app is available on host port `5000` (not `8080`):

* http://127.0.0.1:5000/
* http://127.0.0.1:5000/health

If you get `HTTP 403`, you are probably hitting a different service on port `5000`.

Try a different host port:

```
docker run --rm -p 18080:8080 ruach-readings:latest
curl -i http://127.0.0.1:18080/health
```

Check what is using `5000` on macOS:

```
lsof -nP -iTCP:5000 -sTCP:LISTEN
```

If using Colima, confirm Docker context:

```
docker context ls
docker context use colima
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
    
