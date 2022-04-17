## FastApi Skeleton

A python Fastapi skeleton that is crafted to fit specific needs: Building a simple api-only backend. 

### Features

- Using `json_logging` and FastApi middleware to create jsonl (JSON Lines) log file 
..- Easy to view and query using tools like `jq`
..- Captures errors/exception with stacktrace
..- Produces a log entry for every api call
- Settings setup to feed from `dotenv` style (File or Environment variables) 
..- Port/Listen address
..- Database connection string
..- Log file path (jsonl)
- Database configuration using `SQLAlchemy`
- Suggested code structure
..- Each Api set is served from a separate directory and can be mounted arbitrarily on the main api route
..- utils folder to contain common code like settings/db models ...etc.

### Install / usage

#### Requirements

- Python 3
- Pip

#### Clone the code

```
git clone https://github.com/kefahi/fastapi.git
cd fastapi
```

#### Local / Direct Setup

```
pip install -r backend/requirements.txt
python backend/main.py
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
podman save --quiet -o fastapi-backend.tar backend
gzip fastapi-backend.tar

# Then loaded at the target system
podman load -i fastapi-backend.tar.gz
```
