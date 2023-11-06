import os

import pandas as pd

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
    bucket_name2 = "nptestbkt"
    gcs = NPGCS(
        project_id=project_id, gcp_service_account_path=gcp_service_acc_path
    )
    # read csv
    df = pd.read_csv(
        gcs.download_blob_to_stream(bucket_name, "tests/files/ตัวอย่างไทย.csv")
    )
    print(df)
    # read excel
    df = pd.read_excel(
        gcs.download_blob_to_stream(
            bucket_name, "tests/files/sample-excel.xlsx"
        ),
        engine="openpyxl",
    )
    print(df)
