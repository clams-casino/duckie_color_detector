## Color detector Docker container for duckiebot
Code from for Shao (Mike) Zhang. Just make this clear since my name isn't my Github username.

### To build (from root directory)
```bash
docker -H <duckiebot name>.local build -t colordetector . 
```

### To run
```bash
docker -H <duckiebot name>.local run -it --privileged --rm -e N_SPLITS=<number of horizontal sections> --name color-detector colordetector
```

