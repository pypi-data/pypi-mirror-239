import os
from io import BytesIO

import pandas as pd

import sys
from os.path import abspath, dirname

dir_above = dirname(dirname(abspath(__file__)))
sys.path.insert(0, dir_above)
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
    gcp_service_acc_path = "./scbpt_bq_admin.json"
    bucket_name = "scbpt_lake"
    gcs = NPGCS(project_id=project_id, gcp_service_account_path=gcp_service_acc_path)
    files = gcs.list_blobs(bucket_name='scbpt_lake')
    exp_sec = 60
    for f in files:
        url = gcs.get_signed_url(bucket_name,f['blob_name'],expiration=exp_sec)
        print(f"Within {exp_sec} you can download the file {f['blob_name']} using link {url}")