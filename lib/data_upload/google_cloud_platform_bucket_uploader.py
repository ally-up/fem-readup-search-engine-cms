import glob
import os
from pathlib import Path

from google.cloud import storage


#
# Main
#

class GoogleCloudPlatformBucketUploader:

    def create_public_bucket(self, logger, token_name, project_id, bucket_name, clean=False, quiet=False):
        """
        See https://cloud.google.com/storage/docs/creating-buckets#storage-create-bucket-python
        """

        # Set script path
        file_path = os.path.realpath(__file__)
        script_path = os.path.dirname(file_path)
        config_file_path = os.path.join(script_path, token_name)


        # Check for config file
        if not Path(config_file_path).exists():
            logger.log_line(f"✗️ Google Cloud config not found {config_file_path}")
            return

        # Define storage client
        client = storage.Client.from_service_account_json(
            config_file_path, project=project_id
        )

        bucket = client.bucket(bucket_name=bucket_name)
        bucket.storage_class = "STANDARD"

        if client.lookup_bucket(bucket) != None and clean:
            bucket.delete()

        if client.lookup_bucket(bucket) == None:
            client.create_bucket(bucket, location="eu")

        policy = bucket.get_iam_policy(requested_policy_version=3)
        policy.bindings.append(
            {"role": "roles/storage.objectViewer", "members": {"allUsers"}}
        )

        bucket.set_iam_policy(policy)

    def create_private_bucket(self, logger, token_name, project_id, bucket_name, clean=False, quiet=False):
        """
        See https://cloud.google.com/storage/docs/creating-buckets#storage-create-bucket-python
        """

        # Set script path
        file_path = os.path.realpath(__file__)
        script_path = os.path.dirname(file_path)
        config_file_path = os.path.join(script_path, token_name)

        # Check for config file
        if not Path(config_file_path).exists():
            logger.log_line(f"✗️ Google Cloud config not found {config_file_path}")
            return

        # Define storage client
        client = storage.Client.from_service_account_json(
            config_file_path, project=project_id
        )

        bucket = client.bucket(bucket_name=bucket_name)
        bucket.storage_class = "STANDARD"

        if client.lookup_bucket(bucket) != None and clean:
            bucket.delete()

        if client.lookup_bucket(bucket) == None:
            client.create_bucket(bucket, location="eu")

    def upload_data(self, logger, token_name, data_path, project_id, bucket_name, quiet=False):
        """
        See https://cloud.google.com/storage/docs/creating-buckets#storage-create-bucket-python
        """

        # Set script path
        file_path = os.path.realpath(__file__)
        script_path = os.path.dirname(file_path)
        config_file_path = os.path.join(script_path, token_name)

        # Check for config file
        if not Path(config_file_path).exists():
            logger.log_line(f"✗️ Google Cloud config not found {config_file_path}")
            return

        # Define storage client
        client = storage.Client.from_service_account_json(
            config_file_path, project=project_id
        )

        bucket = client.bucket(bucket_name=bucket_name)
        bucket.storage_class = "STANDARD"

        file_count_total = 0

        for file_path in glob.iglob(f"{data_path}/*"):
            blob = bucket.blob(os.path.basename(file_path))
            blob.upload_from_filename(file_path)

            if not quiet:
                logger.log_line(f"✓️ Uploading {os.path.basename(file_path)}")

            file_count_total += 1

    def upload_file(self, logger, token_name, upload_file_path, project_id, bucket_name, quiet=False):
        """
        See https://cloud.google.com/storage/docs/creating-buckets#storage-create-bucket-python
        """

        # Set script path
        file_path = os.path.realpath(__file__)
        script_path = os.path.dirname(file_path)
        config_file_path = os.path.join(script_path, token_name)

        # Check for config file
        if not Path(config_file_path).exists():
            logger.log_line(f"✗️ Google Cloud config not found {config_file_path}")
            return

        # Define storage client
        client = storage.Client.from_service_account_json(
            config_file_path, project=project_id
        )

        bucket = client.bucket(bucket_name=bucket_name)
        bucket.storage_class = "STANDARD"

        blob = bucket.blob(os.path.basename(upload_file_path))
        blob.upload_from_filename(upload_file_path)

        if not quiet:
            logger.log_line(f"✓️ Uploading {os.path.basename(upload_file_path)}")
