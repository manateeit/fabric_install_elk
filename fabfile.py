from fabric.api import *
from fabric.contrib.files import exists


@task
def installJava8():
    put("./installJava8.sh",".")
    run("chmod +x ./installJava8.sh")
    run("./installJava8.sh")
    run("java -version")


@task
def installElasticSearch():
    run("wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -")
    run('echo "deb http://packages.elastic.co/elasticsearch/2.x/debian stable main" | sudo tee -a /etc/apt/sources.list.d/elasticsearch-2.x.list')
    run("sudo apt-get update")
    run("sudo apt-get -y install elasticsearch")
    put("./elasticsearch.yml","/etc/elasticsearch/elasticsearch.yml", use_sudo=True)
    restartElasticSearch()
    run("sudo update-rc.d elasticsearch defaults 95 10")

@task 
def installKibana():
    # run('echo "deb http://packages.elastic.co/kibana/4.4/debian stable main" | sudo tee -a /etc/apt/sources.list.d/kibana-4.4.x.list')
    # run("sudo apt-get update")
    # run("sudo apt-get -y install kibana")
    put("./kibana.yml" , "/opt/kibana/config/kibana.yml", use_sudo=True)
    restartKibana()
    run("sudo update-rc.d kibana defaults 96 9")



@task
def restartElasticSearch():
    stopElasticSearch()
    startElasticSearch()

@task 
def stopElasticSearch():
    run("sudo service elasticsearch stop")
    
@task 
def startElasticSearch():
      run("sudo service elasticsearch start")
  
@task
def restartKibana():
    stopKibana()
    startKibana()

@task 
def stopKibana():
    run("sudo service kibana stop")
    
@task 
def startKibana():
      run("sudo service kibana start")
  





