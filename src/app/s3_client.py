import aioboto3
from fastapi import UploadFile

from config import settings

class S3Client:
    AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
    AWS_STORAGE_BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME
    AWS_ENDPOINT_URL = settings.AWS_ENDPOINT_URL

    def generate_file_url(self, path: str, filename: str) -> str:
        return f'{self.AWS_ENDPOINT_URL}/{self.AWS_STORAGE_BUCKET_NAME}/{path}{filename}'

    async def upload(self, file: UploadFile, path: str = ""):
        session = aioboto3.Session()
        async with session.client(
            's3',
            endpoint_url=self.AWS_ENDPOINT_URL,
            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
        ) as s3:
            key = f'{path}{file.filename}'
            await s3.upload_fileobj(file.file, self.AWS_STORAGE_BUCKET_NAME, key)

        file_url = self.generate_file_url(path, file.filename)
        return file_url
