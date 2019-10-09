daliuge-pbc
===========

This package implements a workflow for the SDP prototype
based on the DALiuGE execution framework.

Quick start
-----------

These might change depending on your system, etc.
In Ubuntu 18.10 I had to make sure I used a version of k8s/minikube < 1.16,
and that my local /etc/resolv.conf was a symlink to /run/systemd/resolve/resolv.conf.

First, start all the underlying infrastructure::

 minikube start --vm-driver=virtualbox --memory 4096
 helm init
 helm install stable/etcd-operator -n etcd
 helm install [...]/sdp-prototype/deploy/charts/sdp-prototype -n sdp-prototype

 # Currently started manually, but eventually started automatically from sdp-prototype-helm pod
 helm install [...]/daliuge-pbc/deploy/daliuge -n daliuge

 # Check where the etcd service is exposed to the host
 #  These values feed SDP_CONFIG_HOST / SDP_CONFIG_PORT below
 minikube service --url sdp-prototype-etcd-nodeport

 # Check where the dlg-dim is exposed to the host
 #  These values feed DLG_DIM_HOST / DLG_DIM_PORT below
 minikube service --url dlg-dim

 # Now leave the NM log running...
 kubectl logs daliuge-deployment-[...] dlg-nm

In a separate browser open ``$DLG_DIM_HOST:$DLG_DIM_PORT``

On a separate terminal start the Processing Block watcher
that will kick the DALiuGE cluster::

 export SDP_CONFIG_HOST=....
 export SDP_CONFIG_PORT=...
 export DLG_DIM_HOST=...
 export DLG_DIM_PORT=...
 cd [...]/daliuge-pbc
 python -m dlg_workflow.main

In yet another terminal "insert" a Processing Block::

 export SDP_CONFIG_HOST=....
 export SDP_CONFIG_PORT=...
 sdpcfg process dlg-realtime:testdlg:0.0.1
