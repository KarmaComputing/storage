# Storage

Create venv

```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

1. [Install podman](https://podman.io/) & [podman-compose](https://github.com/containers/podman-compose)

2. Start your container locally: `podman-compose up`
3. Visit your app locally: http://127.0.0.1:5000/

## View your app locally

Visit: http://127.0.0.1:5000/

### Rebuild container (locally)
If you make changes to `Dockerfile`, then you need to rebuild your container image. To rebuild the container image:
```
podman-compose build
# or 
podman-compose up --build
```

dokku config:set container-iyklgni LOCAL_DEVELOPMENT_MODE=off

## Deployment notes
If deploying for the first time, the container requires keys to be mounted
for contacting the ceph cluster.

```
dokku storage:mount APP_NAME path-to-ssh-keypaid:path-to-.ssh
dokku ps:restart APP_NAME
```

Debug mode must also be set
```
dokku config:set APP_NAME LOCAL_DEVELOPMENT_MODE=off STORAGE_HOST=10.0.0.1 CEPH_FILESYSTEM_NAME=ceph-filesystem-name
```


