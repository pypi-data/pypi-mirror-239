# Note the need to login to azure to authenticate: this allows a connection to blob storage
# Do this by running the following in the console linked to your python kernel:
# az login

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient  
import pandas as pd

def write_buffer_default_credential(buffer, blob_name, container_name, account_url):
    '''
    Writes a buffer (a store of bytes in memory), which you should have already made and written to, to blob storage

    # Example usage: note you initialise the buffer then write the datafrane to it
    buffer = BytesIO()
    df.to_parquet(buffer, index=False, engine='pyarrow')
    write_buffer_default_credential(buffer, ...)
    '''
    
    credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(account_url, credential=credential)

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Go to the start of the BytesIO object
    buffer.seek(0)

    blob_client.upload_blob(buffer.getvalue(), overwrite = True)



def write_buffer_connection_string(
    buffer,
    blob_name: str,
    container_name: str,
    connection_string: str
) -> None:

    """
    Writes a buffer (a store of bytes in memory), which you should have already made and written to, to blob storage

    Authenticates with a connection string

    # Usage example:
    buffer = BytesIO()
    df.to_parquet(buffer, index=False, engine='pyarrow')
    
    connection_string = 'LONG AND SECRET CONNECTION STRING'
    container_name = "gold-curated"
    blob_name = "bloomberg_daily/parquet/test.parquet"
    write_buffer_connection_string(buffer, 'test.parquet', container_name, connection_string)
    """

    # Create a BlobServiceClient using the Azure connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Get a BlobClient object representing the named blob within the named container
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Go to the start of the BytesIO object
    buffer.seek(0)

    # Create the blob in Azure Blob Storage using the data in buffer
    blob_client.upload_blob(buffer.read(), overwrite=True)

