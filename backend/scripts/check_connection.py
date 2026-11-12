"""Step 1 smoke test: can Python reach MongoDB Atlas, read and write, and how much
of the 512 MB Free-tier quota is already used?

Run from the repo root:
    python -m backend.scripts.check_connection
"""
import sys
from datetime import datetime, timezone

from pymongo.errors import ConfigurationError, OperationFailure, ServerSelectionTimeoutError

from backend.app.config import get_settings
from backend.app.db import get_client, get_db

FREE_TIER_BYTES = 512 * 1024 * 1024


def mb(n: float) -> str:
    return f"{n / 1024 / 1024:,.2f} MB"


def main() -> int:
    settings = get_settings()
    print(f"Environment: {settings.app_env}  |  database: {settings.mongodb_db}")

    try:
        client = get_client()
        client.admin.command("ping")
    except ServerSelectionTimeoutError as e:
        print("\n[FAIL] Could not reach the cluster within 10 s.")
        print("  Most likely: your current IP is not in Atlas -> Network Access,")
        print("  or a firewall/VPN is blocking port 27017.")
        print(f"  Detail: {str(e)[:300]}")
        return 1
    except (ConfigurationError, OperationFailure) as e:
        print("\n[FAIL] Reached Atlas but the connection was rejected.")
        print("  Check the username/password in MONGODB_URI. If the password has")
        print("  special characters (@ : / ? # %), URL-encode them.")
        print(f"  Detail: {e}")
        return 1

    info = client.server_info()
    print(f"[OK] Connected. MongoDB server version {info['version']}")

    db = get_db()

    # Round-trip write -> read -> delete, in a throwaway collection.
    probe = {"probe": True, "at": datetime.now(timezone.utc)}
    inserted_id = db["_healthcheck"].insert_one(probe).inserted_id
    found = db["_healthcheck"].find_one({"_id": inserted_id})
    db["_healthcheck"].delete_one({"_id": inserted_id})
    if not found:
        print("[FAIL] Wrote a document but could not read it back.")
        return 1
    print("[OK] Write / read / delete round trip works.")

    # Storage check. Atlas counts uncompressed data + indexes against the 512 MB.
    stats = db.command("dbStats")
    used = stats.get("dataSize", 0) + stats.get("indexSize", 0)
    print(f"[OK] Collections: {db.list_collection_names() or '(none yet)'}")
    print(f"     Data {mb(stats.get('dataSize', 0))} + indexes {mb(stats.get('indexSize', 0))}"
          f" = {mb(used)} of ~512 MB ({used / FREE_TIER_BYTES:.1%})")

    print("\nStep 1 complete: Python <-> Atlas is working.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
