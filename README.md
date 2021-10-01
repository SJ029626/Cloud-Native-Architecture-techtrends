# Cloud-Native-Architecture-techtrends
TechTrends is an online website used as a news sharing platform, that enables consumers to access the latest news within the cloud-native ecosystem. In addition to accessing the available articles, readers are able to create new media articles and share them.

# Steps to Achieve the Project:
#### 1. Add two endpoints "healthz" and "metrics" in techtrends folder in app.pyf file. Also add logging in the file and test it on your local.
#### 2. After adding the 2 endpoints, now the turn comes of adding the things in docker file. So after adding the required things in docker file.
#### 3. I have here worked on google cloud so therefore launched a machine with 2 vcpus, installed docker.io, update the machine and upgrade it. Also similarly install the k3s in all we are doing complete setup.
```
sudo apt-get update
sudo apt-get upgrade
sudo apt install docker.io
sudo apt-get upgrade

Check Docker Version:
docker --version

curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=v1.20.8-rc1+k3s1 sh 

Check K3S Version:
k3s --version
```
#### After this we will build the docker image:
```
sudo docker build -t sanyamj/techtrends .
sudo docker run -d -p 7111:3111 sanyamj/techtrends

To check docker logs:
you can get container id through : docker ps
sudo docker logs 1a1531b5c0cf
```

#### After this we will setup our pipeline on github. As you can see in .github/workflows. Also if you are using docker or any 3rd tool and you want to set in environment variable go to github repository setting and setup it up there.

#### After doing this we will now come to kubernetes which we have installed through K3S for production grade clusters.
```
sudo kubectl get no
kubectl get all -n sandbox
sudo kubectl apply -f namespace.yaml 
sudo kubectl apply -f service.yaml
sudo kubectl apply -f deploy.yaml
kubectl get all -n prod

To expose it we will have 3 methods:
In Cluster: which we normally map and expose.
Nodeport: kubectl expose deployment techtrends -n prod --type=NodePort --name=prod-service
Loadbalancer: kubectl expose deployment techtrends -n prod --type=LoadBalancer --name=prod-service

Also you can refer this youtube link to check more: https://www.youtube.com/watch?v=1HgKoGjB968

Also we need to open port on google cloud, one can refer this link: https://www.youtube.com/watch?v=1FY0LItJt18&feature=emb_logo
```

#### Now this we have all done through Declaritive approach in kubernetes, Also we have setted up the pipeline in github now. So now to make it more better we will use helm charts. So that for different environment we don't have to make separate file again and again and we can use templates now with the values that we want for each environment.

#### Now after setting up CI pipeline and doing all the things we will setup ArgoCD for continuous delivery. From the following link: https://argo-cd.readthedocs.io/en/stable/ . After installation of ArgoCD now we have to use our github repo link like this: https://github.com/SJ029626/Cloud-Native-Architecture-techtrends.git in UI, you can check out screenshot for more clarity and select the values according to your environment you want to install.

#### Also Remember here we are using the pull based mechanism for all of this and not push based mechanism.

#### Screenshot which show I have complete my project:
![My project completion](https://github.com/SJ029626/Cloud-Native-Architecture-techtrends/blob/main/completion.png)
