import json
import os

from cloudflare_kv import Namespace

kv_namespace = Namespace(
    account_id=os.environ["CF_ACCOUNT_ID"],
    namespace_id=os.environ["CF_NAMESPACE_ID"],
    api_key=os.environ["CF_API_KEY"],
)


if __name__ == "__main__":
    data = kv_namespace.read("data")
    data = json.dumps(data)
    print(data)
