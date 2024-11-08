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

This is the declarative recipe for building the Valkey rock. At the time of recording this demo, we were containerising Valkey 7.2.5 into Ubuntu Jammy, from a snap. But today we already the debian packages in Ubuntu Noble and Oracular, and Valkey 8 is also already available in our current development Ubuntu release - Plucky.
1. `bat rockcraft.yaml`
---
This will create an OCI archive.

2. `rockcraft pack`
---
Before running a container, we convert the OCI archive to the desired runtimes. We first do it for Docker, and test it.

3. `rockcraft.skopeo copy oci-archive:valkey_7.2.5_amd64.rock docker-daemon:valkey:7.2.5`
4. `docker run --rm valkey:7.2.5 --run exec valkey-cli info`
5. `docker run --rm valkey:7.2.5 services`
6. `docker run --rm valkey:7.2.5 plan`

Notice how we use the Pebble entrypoint to execute one-shot commands and also to inspect the container's services without launching them.

---

We then want to deploy it into a Kubernetes cluster. This is our manifest. We will expose Valkey through a Kubernetes Service on port 30001 and deploy the above container with "--protected-mode" disabled, just for the sake of this demo.
7. `bat deployment.yaml`

---

As we did above, we're now going to import the container image into the local MicroK8s image cache.
8. `docker save valkey:7.2.5 > valkey_7.2.5.tar`
9. `microk8s ctr image import valkey_7.2.5.tar`
10. `microk8s ctr images ls | grep valkey`

---

We then apply the above manifest to create the Kubernetes deployment and Valkey service.
11. `kubectl apply -f deployment.yaml`

---

After a few seconds, the Valkey Pod is running and the Service is alive and listening on the 30001 port.
12. `kubectl describe po`
13. `kubectl get svc`
14. `kubectl get po`

---

As we did with Docker above, we can also double-check that Pod produces a similar output to what we saw before.
15. `kubectl exec <pod> -- valkey-cli info`

---

This is optional, but now we are also going to create a 2nd rock: a Chiselled Python3.10 runtime with a Valkey client.
16. do the valkey-client demo (see below)

---

Final cleanup.
17. `kubectl delete -f deployment.yaml`


## Valkey client

We have a very simple Python client for Valkey. It is prepared to use Valkey both as a consumer or publisher of messages.

With the above Valkey deployment active in our local MicroK8s, let's build a 2nd rock. This is the recipe. Note the `bare` base - meaning that we are not shipping the Ubuntu base with this rock. And also note the `python3.10_standard`, where `_standard` refers to a **slice** of Python3.10, and not the entire package. This is a Chiselled rock!
1. `bat rockcraft.yaml`
2. `rockcraft pack`

---

We want to run this with Docker, so let's copy the rock (OCI archive) to the Docker daemon, and do a quick Pebble inspection (`plan`).
3. `rockcraft.skopeo copy oci-archive:valkey-client_7.2.5_amd64.rock docker-daemon:valkey-client:7.2.5`
4. `docker run --rm valkey-client:7.2.5 plan`

---

Now let's start two instances of this image.
The 1st container will _subscribe_ to valkey, and wait for messages to arrive.
5. `docker run --rm --net host valkey-client:7.2.5 -v --args valkey-client -p 30001 -t sub`

---

The 2nd container will also connect to Valkey, but in publisher mode.
6. `docker run --rm --net host -i valkey-client:7.2.5 exec valkey_client -p 30001 -t pub`

---

We can then send messages from one container to the other, via the Valkey deployment that is running on MicroK8s.
7. send a few messages and then STOP

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
