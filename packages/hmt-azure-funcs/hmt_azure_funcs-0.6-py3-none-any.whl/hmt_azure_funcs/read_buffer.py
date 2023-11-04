
# Note the need to login to azure to authenticate: this allows a connection to blob storage
# Do this by running the following in the console linked to your python kernel:
# az login

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from io import BytesIO

def read_buffer_default_credential(blob_name: str, container_name: str, account_url: str):

    ''' Returns a buffer: a bytes object which can be read, eg to read a csv file from blob storage:
    
    buffer = read_parquet_from_container_default_credential(....)
    pd.read_csv(buffer)
     '''
    credential = DefaultAzureCredential()

    blob_service_client = BlobServiceClient(account_url, credential=credential)
    
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    stream = blob_client.download_blob()

    buffer = BytesIO(stream.readall())
    return buffer


def read_buffer_connection_string(
    blob_name: str,
    container_name: str,
    connection_string: str,
):
    '''
    Returns a buffer: a bytes object which can be read

    Authenticates with a connection string

    # Example
    connection_string = 'LONG AND SECRET CONNECTION STRING'container_name = "gold-curated"
    blob_name = "bloomberg_daily/parquet/bloomberg_daily_v4.parquet"

    buffer = read_parquet_from_container(
        blob_name,
        container_name,
        connection_string,
    )

    # Load datafrane
    df = pd.read_parquet(buffer)
    print(df.shape)
    '''

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Download the blob data into a stream
    stream = blob_client.download_blob()

    # Read the stream into a buffer
    buffer = BytesIO(stream.readall())
    return buffer


