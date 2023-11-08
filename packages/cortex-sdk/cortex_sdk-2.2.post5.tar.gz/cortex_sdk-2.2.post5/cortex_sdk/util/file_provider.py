import os
from typing import List, Optional
from ..api.api_resource import APIResource
from ..types.cortex_file import CortexFile
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from enum import Enum

class FileEndpoint(Enum):
    MODEL_DATA    = 'models'
    PIPELINE_DATA = 'pipelines'

class FileProvider(APIResource):
    @classmethod
    def get_files(
        cls,
        endpoint:    FileEndpoint,
        resource_id: str,
        prefix:      Optional[str] = None
    ) -> List[CortexFile]:
        """
        Retrieves a list of files from the Cortex API.
        """
        return cls._generic_get(
            path        = f'/{endpoint.value}/{resource_id}/files/{prefix or ""}',
            return_type = CortexFile
        )

    @classmethod
    def download_files(
        cls, 
        endpoint:    FileEndpoint,
        resource_id: str,
        prefix:      Optional[str] = None, 
        destination: Optional[str] = None
    ):
        """
        Downloads a list of files from the Cortex API.
        """
        def download_task(file: CortexFile):
            download_url = cls._generic_post(
                path = f'/{endpoint.value}/{resource_id}/files/download',
                json = { 'key': file.key }
            ).json()

            dest      = destination or os.getcwd()
            file_path = os.path.join(os.path.abspath(dest), file.key)
            file_data = cls._request_raw('get', download_url['url'])

            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            open(file_path, 'wb').write(file_data.content)

        results = []
        with ThreadPoolExecutor() as executor:
            for i in cls.get_files(endpoint=endpoint, resource_id=resource_id, prefix=prefix):
                results.append(executor.submit(download_task, i))

            for result in as_completed(results):
                result.result()

    
    @classmethod
    def upload_files(
        cls,
        endpoint:    FileEndpoint,
        resource_id: str, 
        source:      str, 
        # destination: Optional[str] = None
    ):
        """
        Uploads a list of files to the Cortex API.
        """

        UPLOAD_PART_SIZE = (1024 * 1024) * 8
        
        def upload_task(file, executor):
            """
            Asynchronously uploads a single file to S3.
            """

            # Create the multi-part object in S3. This needs to happen before
            # the presigned URL is generated.
            key       = file['relative_file_path']
            upload_id = cls._generic_post(
                path = f'/{endpoint.value}/{resource_id}/files/upload',
                json = { 'key': file['relative_file_path'] }
            ).json()['uploadId']
            
            # Split into chunks up front - these chunks are submitted into the
            # thread pool
            parts = []
            with open(file['absolute_file_path'], 'rb') as file:
                while True:
                    # read() will just read up to EOF - once it's out of data, it
                    # will return an empty string
                    data = file.read(UPLOAD_PART_SIZE)
                    if data:
                        parts.append(data)
                    else:
                        break

            # Upload all the individual chunks - each chunk is submitted as an
            # async task, so they will upload concurrently. These can be in
            # flight for multiple files at the same time.
            futures = []
            for index, item in enumerate(parts):
                future = executor.submit(upload_part_task, key, upload_id, index, item)
                futures.append(future)

            # Add parts as they complete. Due to their async nature, it is
            # possible for them to complete out of order...
            merged_upload   = []
            for future in as_completed(futures):
                result = future.result()
                merged_upload.append({
                    'PartNumber': result['partNumber'],
                    'ETag':       result['etag']
                })
            
            # Despite everything being explicitly given a number, the AWS API
            # expects the list to be sequential
            sorted_upload = sorted(merged_upload, key=lambda part: part['PartNumber']) 
            cls._generic_post(
                path =  f'/{endpoint.value}/{resource_id}/files/complete',
                json = {
                    'key':      key,
                    'uploadId': upload_id,
                    'parts':    sorted_upload
                }
            )

        def upload_part_task(key, upload_id, part_number, data):
            """
            Asynchronously uploads a single part of a file to S3.
            """

            part_data = {
                'key':        key,
                'uploadId':   upload_id,
                'partNumber': part_number + 1
            }

            # Each part needs its own presigned URL
            response = cls._generic_post(
                path  =  f'/{endpoint.value}/{resource_id}/files/presign',
                json  = part_data
            ).json()['url']

            # Actually upload the part
            response = cls._request_raw(
                method = 'put',
                url    = response,
                data   = data,
            )
            
            part_data['etag'] = response.headers['ETag']
            return part_data

        #-----------------------------------------------------------------------

        # Generate the list of files to upload up front. Keep the relative path
        # to use for the keys in S3 - this lets us retain the "directory"
        # structure once uploaded.
        files_to_upload = []
        for root, directories, files in os.walk(source):
            for file in files:
                relative_directory = os.path.relpath(root, source)
                if relative_directory == '.':
                    relative_directory = ''

                relative_file_path = os.path.join(relative_directory, file)
                absolute_file_path = os.path.abspath(os.path.join(root, file))

                files_to_upload.append({
                    'relative_directory': relative_directory,
                    'relative_file_path': relative_file_path,
                    'absolute_file_path': absolute_file_path
                })

        # The main thread pool - starts threads on a per file basis
        # These threads can submit more tasks to deal with chunks
        # This uses another executor otherwise you can deadlock this pool
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures         = []
            nested_executor = ThreadPoolExecutor()
            for file in files_to_upload:
                future = executor.submit(upload_task, file, nested_executor)
                futures.append(future)

            wait(futures)
            nested_executor.shutdown()
