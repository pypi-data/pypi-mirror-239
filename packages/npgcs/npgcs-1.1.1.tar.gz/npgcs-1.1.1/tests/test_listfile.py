import os

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

    for blob_name in gcs.list_blobs(bucket_name, prefix="fwd"):
        print(blob_name)
