# Docker registry qiniu storage driver

This is a [docker-registry backend driver][registry-core] for [jss Cloud Storage][jss].

## Usage (recommendation)

Go to [Jss Cloud Storage](http://JAE.JD.COM/) to get your access_key first.

Run docker-registry service by docker container

```
docker run --rm \
  -e SETTINGS_FLAVOR=jssstorage \
  -e JSS_BUCKET=YOUR_BUCKET \
  -e JSS_ACCESSKEY=YOUR_ACCESSKEY \
  -e JSS_SECRETKEY=YOUR_SECRETKEY \
  -e JSS_DOMAIN=YOUR_BUCKET_DOMAIN \
  -p 5000:5000 \
  --name registry \
  zhangwei/docker-registry-jss
```

## Usage via pip

```
# Install pip
apt-get -y install python-pip

# Install deps for backports.lzma (python2 requires it)
apt-get -y install python-dev liblzma-dev libevent1-dev

# Install docker-registry
pip install docker-registry

# finally
pip install qiniu docker-registry-driver-jss

export DOCKER_REGISTRY_CONFIG=/usr/local/lib/python2.7/dist-packages/docker-registry-driver-jss/config/config_jss.yml
export SETTINGS_FLAVOR=jssstorage

export JSS_BUCKET=YOUR_BUCKET
export JSS_ACCESSKEY=YOUR_ACCESSKEY
export JSS_SECRETKEY=YOUR_SECRETKEY
export JSS_DOMAIN=YOUR_BUCKET_DOMAIN
docker-registry
```

## Contributing

In order to verify what you did is ok, just run `pip install tox; tox`. This will run the tests
provided by [`docker-registry-core`][registry-core].

For more information, plz check [`docker-registry-readme`][registry-readme]

[registry-core]: https://github.com/dotcloud/docker-registry/tree/master/depends/docker-registry-core
[jae]: http://JAE.JD.COM/
[registry-readme]: https://github.com/docker/docker-registry/blob/master/README.md