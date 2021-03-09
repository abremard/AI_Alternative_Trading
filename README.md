# AI_Alternative_Trading

[Project documentation](https://htmlpreview.github.io/?https://github.com/abremard/AI_Alternative_Trading/blob/main/src/html/src/index.html)

## Installation

### Setup virtual environment
To create virtual environment, go to project root and run following command:
```python3 -m venv aiat```
On Windows, to activate, run:
``./aiat/Scripts/Activate.ps1``
To install all necessary requirements, run:
``pip install -r src/requirements.txt``

### Setup Docker Elasticsearch container
You will need to have docker installed on your machine before pulling the elastic search image.
On Windows, open your WSL and run to pull elasticsearch image:
``docker pull docker.elastic.co/elasticsearch/elasticsearch:7.11.1``
Start a single node cluster
``docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.11.1``


### Setup Docker Kibana container
On Windows, open your WSL and run to pull kibana image:
``docker pull docker.elastic.co/kibana/kibana:7.11.1``
Now create a Kibana container that's linked to your elasticsearch container:
``docker run --link YOUR_ELASTICSEARCH_CONTAINER_NAME_OR_ID:elasticsearch -p 5601:5601 docker.elastic.co/kibana/kibana:7.11.1``

You're all set, now run both containers and start scraping!