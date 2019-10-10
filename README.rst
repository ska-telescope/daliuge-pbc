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

Start now the sdp-prototype chart pointing to the daligue-pbc repository,
and the daliuge-workflow chart to start watching for incoming Processing Blocks::

 helm install [...]/sdp-prototype/deploy/charts/sdp-prototype -n sdp-prototype --set helm_deploy.chart_repo.url=https://github.com/ska-telescope/daliuge-pbc.git,helm_deploy.chart_repo.path=deploy
 helm install [...]/daliuge-pbc/deploy/workflow -n dlg-workflow
 kubectl get pods --watch
 [...]

Now "create" a Processing Block,
which will kick the DALiuGE cluster::

 ETCD_URL=`minikube service --url sdp-prototype-etcd-nodeport`
 export SDP_CONFIG_HOST=`echo $ETCD_URL | sed 's,http://\(.*\):.*,\1,'`
 export SDP_CONFIG_PORT=`echo $ETCD_URL | sed 's,http://.*:\(.*\),\1,'`
 sdpcfg process dlg-realtime:testdlg:0.0.1

Once this happens a new ``daliuge-deployment`` helm release
should be created and a Processing Block will eventually
start executing in there::

 # Open $DIM_URL in a browser and leave the dlg-nm log running
 DIM_URL=`minikube service --url dlg-dim -n sdp`
 DLG_POD=`kubectl get pods -o name -l app.kubernetes.io/name=daliuge -n sdp`
 DLG_WORKFLOW_POD=`kubectl get pods -o name -l app.kubernetes.io/name=daliuge-workflow`
 kubectl logs -f $DLG_WORKFLOW_POD
 kubectl logs -f -n sdp $DLG_POD dlg-nm
