from minio import Minio


class MinioRepository:
    def __init__(self, *, url, access_key, secret_key, bucket_name):
        self.client = Minio(
            url,
            access_key=access_key,
            secret_key=secret_key,
            secure=False,
        )
        self.bucket_name = bucket_name

    def create_bucket_if_not_exists(self):
        if self.client.bucket_exists(self.bucket_name):
            return
        self.client.make_bucket(self.bucket_name)

    def upload_file(self, file_name, data, ln):
        self.client.put_object(self.bucket_name, file_name, data, ln)

    def get_file(self, file_name):
        return self.client.get_object(self.bucket_name, file_name)
