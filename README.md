

## Overview

* The model training is in `src/eda_modeling.EDA.ipynb`
* Training artifacts are `assets/modeling.pickle` and `assets/scaler.pickle`
* The code for model serving are in `src/serving/app.py` and `Dockerfile`. For how to serve, see instructions below.

## Serve model from docker container

Requiremnts:
- Docker runtime for building and running container running model serving
- `curl` for making model requests

```shell
# Build and launch model server
docker build -t assignment .
docker run -p 5000:5000 assignment
```
Then in another shell session run
```shell
# Make a predicition
curl -X POST -H "Content-Type: application/json" -d '{"perimeter_worst": 59.16, "symmetry_worst": 0.2871  , "texture_worst": 30.37}' http://localhost:5000/predict
```
You should get a response like `{"response":{"body":{"class":"benign","probability":0.51}}}`.

See also example requests in `src/serving/Example Requests.ipynb`.


## Serve model without docker
This is mainly useful for quick testing.

Requirements:
- `poetry` for installing the python virtual environment running model serving
- `curl` for making model requests

```shell
# Build virtual env and launch model server
poetry install
poetry run python src/serving/app.py
```

Request a prediction as described above.

