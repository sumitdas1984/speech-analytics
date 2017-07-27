#!/usr/bin/python

import boto
import gcs_oauth2_boto_plugin
import os
import shutil
import StringIO
import tempfile
import time

# URI scheme for Cloud Storage.
GOOGLE_STORAGE = 'gs'
# URI scheme for accessing local files.
LOCAL_FILE = 'file'

# Fallback logic. In https://console.cloud.google.com/
# under Credentials, create a new client ID for an installed application.
# Required only if you have not configured client ID/secret in
# the .boto file or as environment variables.
CLIENT_ID = 'GOOGZE2B55PJXZ2MK4JP'
CLIENT_SECRET = 'lzX+AJf0kWVhmL1OXx76wAm7pKa3Iy1UfA6F37jL'
gcs_oauth2_boto_plugin.SetFallbackClientIdAndSecret(CLIENT_ID, CLIENT_SECRET)

now = time.time()
CATS_BUCKET = 'cats-%d' % now
DOGS_BUCKET = 'dogs-%d' % now

# Your project ID can be found at https://console.cloud.google.com/
# If there is no domain for your project, then project_id = 'YOUR_PROJECT'
# project_id = 'YOUR_DOMAIN:YOUR_PROJECT'
project_id = 'speechapi'

for name in (CATS_BUCKET, DOGS_BUCKET):
	# Instantiate a BucketStorageUri object.
	uri = boto.storage_uri(name, GOOGLE_STORAGE)
	# Try to create the bucket.
	try:
		# If the default project is defined,
		# you do not need the headers.
		# Just call: uri.create_bucket()
		header_values = {"x-goog-project-id": project_id}
		uri.create_bucket(headers=header_values)

		print 'Successfully created bucket "%s"' % name
	except boto.exception.StorageCreateError, e:
		print 'Failed to create bucket:', e