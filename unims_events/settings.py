LOG_ENABLED = True
LOG_LEVEL = "DEBUG" # CRITICAL, ERROR, WARNING, INFO, DEBUG

MEMUSAGE_LIMIT_MB = 0

ROBOTSTXT_OBEY = True
USER_AGENT = "Scrapy (+https://github.com/codeformuenster/event-api)"
BOT_NAME = "unims-events"

SPIDER_MODULES = ["unims_events.spiders"]

# FEED_STORAGES = {}

FEED_EXPORTERS = {
    "minio": "unims_events.exporter_minio.JsonItemMinioExporter",
}
FEED_FORMAT = "minio"
FEED_EXPORT_ENCODING = "utf-8"
MINIO_ACCESS_KEY_ID = "minio"
MINIO_SECRET_ACCESS_KEY = "minio123"
MINIO_SSL = True
# FEED_URI = "https://minio.codeformuenster.org/unims-events-test2"
FEED_URI = "minio.codeformuenster.org/unims-events-test2"
