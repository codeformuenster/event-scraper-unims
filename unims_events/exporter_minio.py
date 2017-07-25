from scrapy.exporters import JsonLinesItemExporter
from scrapy.utils.serialize import ScrapyJSONEncoder
from scrapy.conf import settings
import logging

from minio import Minio
import minio.error
import hashlib
import json
import io

# FIXME check https://github.com/scrapy/scrapy/blob/master/scrapy/extensions/feedexport.py#L94

class JsonItemMinioExporter(JsonLinesItemExporter):

    def __init__(self, uri, **kwargs):
        # logging.debug(f"uri: \"{uri}\"")
        self._configure(kwargs, dont_fail=True)
        self.bucket = settings.get("MINIO_BUCKET", "unims-events-test")
        kwargs.setdefault("ensure_ascii", not self.encoding)
        self.encoder = ScrapyJSONEncoder(**kwargs)

        logging.debug("Initializing Minio-Client")
        self.minioClient = Minio("minio.codeformuenster.org",
                                 access_key=settings.get("MINIO_ACCESS_KEY_ID", "minio"),
                                 secret_key=settings.get("MINIO_SECRET_ACCESS_KEY", "minio123"),
                                 secure=settings.getbool("MINIO_SSL", True))

    def export_item(self, item):
        itemdict = dict(self._get_serialized_fields(item))
        data = self.encoder.encode(itemdict).encode()
        logging.debug("Trying to export to Minio")
        try:
            data_hash = hashlib.shake_256(data).hexdigest(32)
            self.minioClient.put_object(self.bucket,
                                        f"{data_hash}.json",
                                        io.BytesIO(data),
                                        io.BytesIO(data).getbuffer().nbytes,
                                        content_type="application/json")
        except minio.error.ResponseError as err:
            logging.error(err)
            raise

    def start_exporting(self):
        try:
            logging.debug(f"Creating bucket with name: \"{self.bucket}\"")
            self.minioClient.make_bucket(self.bucket)
        except minio.error.BucketAlreadyOwnedByYou as err:
            pass
        except minio.error.BucketAlreadyExists as err:
            pass
        except minio.error.ResponseError as err:
            logging.error(err)
            raise
