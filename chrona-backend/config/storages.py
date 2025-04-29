from storages.backends.s3boto3 import S3StaticStorage, S3Boto3Storage

class S3StaticFileStorage(S3StaticStorage):
    location = "static"

class S3MediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False
