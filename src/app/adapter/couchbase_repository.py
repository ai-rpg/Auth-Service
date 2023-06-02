
from datetime import timedelta
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions, ClusterTimeoutOptions, QueryOptions

import json

from config import CB_USERNAME, CB_PASSWORD, CB_BUCKET_NAME, CB_CLIENT_COLLECTION, CB_CLUSTER
from logger import log

class CouchbaseRepository():

    def __init__(self):
        auth = PasswordAuthenticator(
            CB_USERNAME,
            CB_PASSWORD
        )
        self.cluster = Cluster(CB_CLUSTER, ClusterOptions(auth))
        self.cluster.wait_until_ready(timedelta(seconds=60))
        self.cb = self.cluster.bucket(CB_BUCKET_NAME)
        self.cb_coll = self.cb.scope("_default").collection(CB_CLIENT_COLLECTION)
        self.cb_coll_default = self.cb.default_collection()
        try:
            self.cluster.query("CREATE PRIMARY INDEX on {CB_BUCKET_NAME}._default.{CB_COLLECTION}")
        except QueryIndexAlreadyExistsException:
            log.warning("Index already exists")

    def get(self):
        pass
