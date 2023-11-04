
# Note the need to login to azure to authenticate: this allows a connection to blob storage
# Do this by running the following in the console linked to your python kernel:
# az login

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import pandas as pd
from io import BytesIO

def read_parquet_from_container_default_credential(blob_name: str, container_name: str, account_url: str) -> pl.DataFrame:

    credential = DefaultAzureCredential()

    blob_service_client = BlobServiceClient(account_url, credential=credential)
    
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    stream = blob_client.download_blob()

    buffer = BytesIO(stream.readall())
    return pd.read_parquet(buffer)

#account_url = "https://hmtdatasciencedevrga07f.blob.core.windows.net/"
#read_parquet_from_container('output.parquet', container_name, account_url)
