from google.cloud import storage
import glob
import os

# Upload files to storage for testing
client = storage.Client()
here = os.path.dirname(os.path.abspath(__file__))

bucket_name = "snakemake-testing"

try:
    bucket = client.get_bucket(bucket_name)
except:
    bucket = client.create_bucket(bucket_name)

# key, full path, value: upload path in storage
filenames = dict()

for x in os.walk(os.path.join(here, 'scripts')):
    for name in glob.glob(os.path.join(x[0], '*')):
        if not os.path.isdir(name):
            filenames[name] = name.replace(here + os.path.sep, '')


# Upload files in script and base gooogle life sciences folder
for filename, remotename in filenames.items():
    blob = bucket.blob(remotename)

    if not blob.exists():
        print("Uploading %s to %s" %(remotename, bucket_name))
        with open(filename, 'r') as filey:
            blob.upload_from_string(
                filey.read(),
                content_type="text/plain")
