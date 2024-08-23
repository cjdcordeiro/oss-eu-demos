<!-- source set-demo-env -->

# Flask

Ref: <https://documentation.ubuntu.com/rockcraft/en/stable/tutorials/getting-started-with-flask/>

## 0.1

1. use the template files
2. `rockcraft init --profile flask-framework`
3. `bat rockcraft.yaml`
4. `rockcraft expand-extensions`
5. `rockcraft pack`
6. `du -sh flask-hello-world_0.1_amd64.rock`
7. `rockcraft.skopeo copy oci-archive:flask-hello-world_0.1_amd64.rock docker-daemon:flask:0.1`
8. `docker images flask:0.1`
9. `docker run --rm -p 8000:8000 flask:0.1`

## 0.2

1. `docker run --rm flask:0.1 exec perl -e 'print "hello\n"''`

    Why do we need such utilities?

2. change `base` to `bare`, and update version to 0.2
3. `rockcraft pack`
4. `du -sh flask-hello-world_0.2_amd64.rock`
5. `rockcraft.skopeo copy oci-archive:flask-hello-world_0.2_amd64.rock docker-daemon:flask:0.2`
6. `docker images flask:0.2`
7. `docker run --rm flask:0.2 exec perl -e 'print "hello\n"'`
8. `docker run --rm -p 8000:8000 flask:0.2`

# Valkey

1. `bat rockcraft.yaml`
2. `rockcraft pack`
3. `rockcraft.skopeo copy oci-archive:valkey_7.2.5_amd64.rock docker-daemon:valkey:7.2.5`
4. `docker run --rm valkey:7.2.5 --run exec valkey-cli info`
5. `docker run --rm valkey:7.2.5 services`
6. `docker run --rm valkey:7.2.5 plan`
7. `bat deployment.yaml`
8. `docker save valkey:7.2.5 > valkey_7.2.5.tar` for importing into microk8s
9. `microk8s ctr image import valkey_7.2.5.tar` import image to local microk8s image cache - might help to restart microk8s
10. `microk8s ctr images ls | grep valkey`
11. `kubectl apply -f deployment.yaml`
12. `kubectl describe po` might need to re-import the image
13. `kubectl get svc` note the nodeport
14. `kubectl get po`
15. `kubectl exec <pod> -- valkey-cli info`
16. do the valkey-client demo (see below)
17. `kubectl delete -f deployment.yaml`

## Valkey client

1. `bat rockcraft.yaml`
2. `rockcraft pack` (may need a clean)
3. `rockcraft.skopeo copy oci-archive:valkey-client_7.2.5_amd64.rock docker-daemon:valkey-client:7.2.5`
4. `docker run --rm valkey-client:7.2.5 plan`
5. `docker run --rm --net host valkey-client:7.2.5 -v --args valkey-client -p 30001 -t sub`
6. open split the terminal
7. `docker run --rm --net host -i valkey-client:7.2.5 exec valkey_client -p 30001 -t pub`
8. send a few messages and then STOP

# Python runtime

Open all side by side

## rock

1. `cd python-rock`
2. `bat rockcraft.yaml`
3. `rockcraft pack`
4. `du -sh python_3.11_amd64.rock`
5. `rockcraft.skopeo copy oci-archive:python_3.11_amd64.rock docker-daemon:python-rock:latest`
6. `docker run --rm python-rock exec python3.11 -c 'print("hello")'`

## baseless rock

1. `cd baseless-python-rock`
2. `bat rockcraft.yaml`
3. `rockcraft pack`
4. `du -sh baseless-python_3.11_amd64.rock`
5. `rockcraft.skopeo copy oci-archive:baseless-python_3.11_amd64.rock docker-daemon:baseless-python-rock:latest`
6. `docker run --rm baseless-python-rock exec python3.11 -c 'print("hello")'`

## chiselled rock

1. `cd chiselled-python-rock`
2. `bat rockcraft.yaml`
3. `rockcraft pack`
4. `du -sh chiselled-python_3.11_amd64.rock`
5. `rockcraft.skopeo copy oci-archive:chiselled-python_3.11_amd64.rock docker-daemon:chiselled-python-rock:latest`
6. `docker run --rm chiselled-python-rock exec python3.11 -c 'print("hello")'`

# CIS/STIG

**You need a `tailoring` folder with the tailoring XML files for this.**

For any 22.04-based rock above:

1. `source ../set-demo-env`
2. `cis-audit <image-name>`
3. `stig-audit <image-name>`
4. `open reports/*html`
