import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Create Client
load_dotenv()

# url: str = os.getenv("SUPABASE_URL")
# key: str = os.getenv("SUPABASE_KEY")
# supabase: Client = create_client(url, key)

url: str = 'https://cwqyhomdhwpkbpftqhlm.supabase.co'
key: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3cXlob21kaHdwa2JwZnRxaGxtIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5ODI1MDA3MiwiZXhwIjoyMDEzODI2MDcyfQ.A7dr4NoSpGCjBUp-zYu8ElhnbukCcJuB6U6PSSCRU1I'
supabase: Client = create_client(url, key)

def downloadApi(filename: str, dir='tmp/', bucketDir='JobQueue/'):
    """
    Download a file from a remote storage bucket and save it locally.

    Args:
        filename (str): The name of the file to be downloaded.
        dir (str, optional): The local directory where the file will be saved (default is 'pyDir').
        bucketDir (str, optional): The directory in the storage bucket where the file is located (default is 'JobQueue/').

    Returns:
        None

    Note:
    - This function is designed to download a file from a remote storage bucket (e.g., Supabase) and save it locally.
    - The 'filename' argument specifies the name of the file to be downloaded.
    - The 'dir' argument (defaulting to 'tmp/') specifies the local directory where the downloaded file will be saved.
    - The 'bucketDir' argument (defaulting to 'JobQueue/') specifies the directory in the remote storage bucket where
      the file is located.
    - The function constructs the full local path and downloads the file, saving it locally in binary mode ('wb+').
    - Make sure to have the appropriate access and credentials to access the remote storage bucket.

    Example Usage:
    downloadApi('example_file', dir='myLocalDir/', bucketDir='CustomBucket/')

    Details:
    - This function is used to download files from a remote storage bucket and is often used to retrieve files for
      local processing.
    - The 'dir' argument allows you to specify a different local directory where the downloaded file should be saved.
    - The 'bucketDir' argument allows you to specify a different directory within the storage bucket where the file
      is located.
    """
    # Construct the full path to save the downloaded file locally
    path = dir + filename + '.inp'

    # Open a file for writing in binary mode ('wb+')
    with open(path, 'wb+') as f:
        # Download the file from the remote storage bucket (e.g., Supabase)
        res = supabase.storage.from_('ivette-bucket').download(bucketDir + filename)
        
        # Write the downloaded content to the local file
        f.write(res)



def uploadFile(filename: str, id: str, bucketDir: str, bucketName='ivette-bucket', localDir='tmp/'):
    """
    Upload a local file to a remote storage bucket.

    Args:
        filename (str): The name of the local file to be uploaded.
        id (str): The unique identifier associated with the file (e.g., job ID).
        bucketDir (str): The directory in the storage bucket where the file will be stored.
        bucketName (str, optional): The name of the remote storage bucket (default is 'ivette-bucket').
        localDir (str, optional): The local directory where the file is located (default is 'tmp/').

    Returns:
        None

    Note:
    - This function is used to upload a local file to a remote storage bucket (e.g., Supabase).
    - The 'filename' argument specifies the name of the local file to be uploaded.
    - The 'id' argument specifies a unique identifier associated with the file, often used for naming within the bucket.
    - The 'bucketDir' argument specifies the directory in the storage bucket where the file will be stored.
    - The 'bucketName' argument (defaulting to 'ivette-bucket') specifies the name of the remote storage bucket.
    - The 'localDir' argument (defaulting to 'tmp/') specifies the local directory where the file is located.
    - The function reads the local file, creates a path in the remote storage bucket, and uploads the file.

    Example Usage:
    uploadFile('A1.log', 'clod1k4zd0000d2rh3z5l3dt1', 'Calculations/', 'my-storage-bucket', 'myLocalDir/')

    Details:
    - This function is often used to upload files to remote storage for sharing, archiving, or processing.
    - The 'bucketName' and 'localDir' arguments allow you to specify the target storage bucket and local file directory.
    - The 'bucketPath' is constructed using 'bucketDir' and 'id' to specify the exact location within the storage bucket.
    - The file is read in binary mode ('rb') and uploaded to the specified path in the remote storage bucket.
    - Ensure that you have the necessary access and credentials to upload to the remote storage bucket.
    """
    filepath = localDir + filename
    bucketPath = bucketDir + id

    # Open the local file for reading in binary mode ('rb')
    with open(filepath, 'rb') as f:
        # Upload the file to the specified path in the remote storage bucket
        supabase.storage.from_(bucketName).upload(
            file=f, path=bucketPath, file_options={"content-type": "text/html"})

