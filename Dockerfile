FROM alpine:3.15

# Optional external mount points
VOLUME ["/home"]

# Copy sample project python source code
ADD backend /home/backend/

# Install required run-time packages
RUN apk add --no-cach python3 py3-requests libpq 

# Install required pips (from backend/requirments.txt) along with disposable build tools
RUN apk add --no-cache --virtual devstuff musl-dev py3-wheel python3-dev gcc g++ libpq-dev py3-pip \
  && pip3 install -r /home/backend/requirements.txt \
  && pip3 cache purge \
  && apk del --no-cache devstuff

#CMD ["python3", "/home/backend/backend.py"]
CMD ["ash"]
