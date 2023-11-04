
# Note the need to login to azure to authenticate: this allows a connection to blob storage
# Do this by running the following in the console linked to your python kernel:
# az login

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient  
import pandas as pd

def write_parquet_to_container_default_credential(df, blob_name, container_name, account_url):
    
    credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(account_url, credential=credential)

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    buffer = BytesIO()
    df.to_parquet(buffer)

    blob_client.upload_blob(buffer.getvalue(), overwrite = True)

# Example usage
#df = pd.DataFrame({"col1": [1,2,3,4]}) 
#write_parquet_to_container(df, "output.parquet", container_name, account_url)
