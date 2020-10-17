## Color detector Docker container for duckiebot

### To build (from root directory)
```bash
docker -H <duckiebot name>.local build -t colordetector . 
```

### To run
```bash
docker -H <duckiebot name>.local run -it --rm -e N_SPLITS=<number of horizontal sections> --name color-detector colordetector
```

