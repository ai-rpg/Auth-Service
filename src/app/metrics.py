from prometheus_client import Summary, Gauge, Counter, Info

PORT = Info("port", "port")
NEW_USER_ENDPOINT_CALLED = Counter("new_user_endpoint_called", "new user endpoint called")
