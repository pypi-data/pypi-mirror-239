import os
from enum import Enum


# field which is used to store meta information about the file in ElasticSearch, e.g. path, extension, type
META_FIELD = "properties"
CONTENT_FIELD = "content"
DOC_TYPE_FIELD = "doc_type"
ES_URL = os.getenv("DOCPARSER_ES_URL", "http://localhost:9200")
ELASTIC_BULK_BATCH_SIZE = 100
ELASTIC_GLOBAL_TIMEOUT = 30
BROKER_URL = "redis://localhost:6379/0"
RESULT_BACKEND_URL = "redis://localhost:6379/0"

class DocType(Enum):
    E_MAIL = "email"
    ATTACHMENT = "attachment"
    DOCUMENT = "document"
