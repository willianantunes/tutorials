from elasticsearch import Elasticsearch

from es_watcher import settings

single_host = {
    "host": settings.ELASTICSEARCH_HOST,
    "port": settings.ELASTICSEARCH_PORT,
    "use_ssl": settings.ELASTICSEARCH_USE_SSL,
}
if settings.ELASTICSEARCH_USER:
    single_host["http_auth"] = (settings.ELASTICSEARCH_USER, settings.ELASTICSEARCH_PASSWORD)

es_client = Elasticsearch(hosts=[single_host])
