import os
from io import BytesIO

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
    gcp_service_acc_path = "./tests/scbpt_bq_admin.json"
    bucket_name = "scbpt_lake"
    gcs = NPGCS(project_id=project_id, gcp_service_account_path=gcp_service_acc_path)
    # read csv
    df = pd.read_csv(r"tests\files\ตัวอย่างไทย.csv")
    print(df)

    # save it as parquet which is binary
    fo = BytesIO()
    df.to_parquet(fo, engine="pyarrow")  # works
    # df.to_parquet(fo, engine="fastparquet") # not working
    fo.seek(0)
    gcs.upload_blob_from_stream(
        bucket_name, file_obj=fo, destination_blob_name="hello.parquet"
    )
    print("job is done")
