from fabric.api import *
from fabric.contrib.files import exists
import time


@task
def installJava8():
    put("./installJava8.sh",".")
    run("chmod +x ./installJava8.sh")
    run("./installJava8.sh")
    run("java -version")

@task
def updateRepo():
    run("wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -")
    run('echo "deb http://packages.elastic.co/elasticsearch/2.x/debian stable main" | sudo tee -a /etc/apt/sources.list.d/elasticsearch-2.x.list')
    run('echo "deb http://packages.elastic.co/kibana/4.4/debian stable main" | sudo tee -a /etc/apt/sources.list.d/kibana-4.4.x.list')
    run("echo 'deb http://packages.elastic.co/logstash/2.2/debian stable main' | sudo tee /etc/apt/sources.list.d/logstash-2.2.x.list")
    run("sudo apt-get update")


@task
def installElasticSearch():
    run("sudo apt-get -y install elasticsearch")
    put("./elasticsearch.yml","/etc/elasticsearch/elasticsearch.yml", use_sudo=True)
    restartElasticSearch()
    run("sudo update-rc.d elasticsearch defaults 95 10")

@task 
def installKibana():
    run("sudo apt-get -y install kibana")
    put("./kibana.yml" , "/opt/kibana/config/kibana.yml", use_sudo=True)
    restartKibana()
    run("sudo update-rc.d kibana defaults 96 9")

@task 
def installNginx():
    run("sudo apt-get -y install nginx apache2-utils")
    sudo("sudo htpasswd -c /etc/nginx/htpasswd.users kibanaadmin")
    put("nginxSitesDefault", "/etc/nginx/sites-available/default", use_sudo=True)
    restartNginx()

@task
def installLogstash():
    run("sudo apt-get install logstash")
    put("./genSSLLogstash.sh",".")
    run("chmod +x ./genSSLLogstash.sh")
    run("./genSSLLogstash.sh")
    put("./02-beats-input.conf" , "/etc/logstash/conf.d/02-beats-input.conf", use_sudo=True)
    put("./10-syslog-filter.conf" , "/etc/logstash/conf.d/10-syslog-filter.conf", use_sudo=True)
    put("./30-elasticsearch-output.conf", "/etc/logstash/conf.d/30-elasticsearch-output.conf", use_sudo=True)
    run("sudo service logstash configtest")
    time.sleep(2)
    run("sudo service logstash restart")
    time.sleep(2)
    run("sudo update-rc.d logstash defaults 96 9")
    get("/etc/pki/tls/certs/logstash-forwarder.crt", ".", use_sudo=True)



@task
def loadKibanaDashboards():
    run("curl -L -O https://download.elastic.co/beats/dashboards/beats-dashboards-1.1.0.zip")
    run("sudo apt-get install -y unzip")
    run("unzip beats-dashboards-*.zip")
    run("cd beats-dashboards-* && ./load.sh")
    run("curl -O https://gist.githubusercontent.com/thisismitch/3429023e8438cc25b86c/raw/d8c479e2a1adcea8b1fe86570e42abab0f10f364/filebeat-index-template.json")
    run("curl -XPUT 'http://localhost:9200/_template/filebeat?pretty' -d@filebeat-index-template.json")


@task
def restartElasticSearch():
    stopElasticSearch()
    time.sleep(5)
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
    time.sleep(5)
    startKibana()
    time.sleep(5)
    statusKibana()

@task 
def stopKibana():
    run("sudo service kibana stop")
    
@task 
def startKibana():
      run("sudo service kibana start")

@task 
def statusKibana():
      run("sudo service kibana status")

@task
def restartNginx():
    stopNginx()
    time.sleep(5)
    startNginx()
  

@task 
def stopNginx():
    run("sudo service nginx stop")
    
@task 
def startNginx():
      run("sudo service nginx start")




