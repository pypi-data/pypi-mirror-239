import os
from time import perf_counter

from npgcs import NPGCS


def list_all_files(mypath):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(mypath):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            files.append(fp)
    return files


if __name__ == "__main__":
    fp = "./tests/files"
    files = list_all_files(fp)

    project_id = "scbpt-349407"
    gcp_service_acc_path = "./tests/scbpt-owner.json"
    bucket_name = "scbpt_lake"
    gcs = NPGCS(
        project_id=project_id, gcp_service_account_path=gcp_service_acc_path
    )

    # syncronous
    start = perf_counter()
    for file in files:
        gcs.upload_blob(bucket_name, file, file)
    end = perf_counter()
    print(f"Time taken: {end - start} seconds")

    # asyncronous
    start = perf_counter()
    # gcs.async_upload_blob(bucket_name, files)
    end = perf_counter()
    print(f"Time taken: {end - start} seconds")
