
https://doc.scrapy.org/en/latest/topics/feed-exports.html

s3://mybucket/scraping/feeds/%(name)s/%(time)s.json

s3://aws_key:aws_secret@mybucket/path/to/export.csv



https://github.com/minio/minio/issues/1025

>>> import boto3
>>> s3 = boto3.resource('s3', endpoint_url='http://localhost:9000')
>>> for bucket in s3.buckets.all():
...     print(bucket.name)


https://stackoverflow.com/questions/8911162/scrapy-custom-exporter/41973194

https://bitbucket.org/drozdyuk/scrapy_quotes/src/94b44753cd33e8bd996d4e292a4666b6f7f682a0/scrapy_quotes/pipelines.py?at=master&fileviewer=file-view-default
