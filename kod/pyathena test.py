from pyathena import connect
import pandas as pd
con = connect(
    s3_staging_dir="s3://gpw-tracker-bucket/athena-results/",
    region_name="eu-north-1",
    schema_name="gpw-tracker_db"
)
df = pd.read_sql("SELECT * FROM bronze LIMIT 5", con)
print(df)