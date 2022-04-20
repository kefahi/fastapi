## FastApi Skeleton

A python Fastapi skeleton that is crafted to fit specific needs: Building a simple api-only backend. 

### Features

- Using `json_logging` and FastApi middleware to create jsonl (JSON Lines) log file 
  - Easy to view and query using tools like `jq`
  - Captures errors/exception with stacktrace
  - Produces a log entry for every api call with extensible details
- Settings setup to feed from `dotenv` style (File or Environment variables) 
  - Port/Listen address
  - Database connection string
  - Log file path (jsonl)
- Database configuration using `SQLAlchemy`
- Suggested code structure
  - `api` folder: apis are broken into api-sets, each Api set is served from a separate directory and can be mounted arbitrarily on the main api route. e.g. /my1stapiset, /2ndapiset ...etc.
  - `utils` folder: contains common code like settings, db models ...etc.
- Optimized / small footprint container image based on barebone Alpine 3.15. The skeleton image size containing the code + python + depdedent python modules (the file fastapi-backend.tar.gz below) is only 23MB. This also makes it ideal for air-gapped deployements (copying the image to a server that doesn't have internet access). 

### Install / usage

#### Requirements

- git
- python 3
- pip

Optional:

- podman
- gzip


#### Clone the code

```
git clone https://github.com/kefahi/fastapi.git
cd fastapi
```

#### Local / Direct Setup

```
pip install -r backend/requirements.txt

# Create logs folder (path can be configured in sample.env)
mkdir ../logs/

# To run:
BACKEND_ENV=sample.env python backend/main.py
# or 
./run.sh
```

#### Using Podman/Container

```
# Build
podman build -t fastapi-backend .

# Run 
podman run --name fastapi-backend --rm \
  -e LOG_PATH=/var/log/ \
  -e DATABASE_URL="postgresql://MYDBUSER:MYPASS@DBSERVERIP/DB" \
  -p 127.0.0.1:8080:8080/tcp \
  -it fastapi-backend \
  /usr/bin/python3 /home/backend/main.py
  
# Command line access inside the container
podman exec -it fastapi-backend ash

# The image can be saved to a file for off-line deployement
podman save --quiet backend | gzip > fastapi-backend.tar.gz

# Then loaded at the target system
podman load -i fastapi-backend.tar.gz
```


