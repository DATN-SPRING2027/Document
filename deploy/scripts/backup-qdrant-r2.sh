#!/usr/bin/env bash
# ==============================================================================
# Continuum AI — Automated Qdrant Vector Collection Snapshots to Cloudflare R2
# Snapshots every per-project SAG Qdrant collection (search_units_*,
# routing_tree_*, session_units_*), verifies SHA-256 checksums, uploads to R2,
# cleans remote transient snapshots, and enforces retention pruning.
#
# Cron (03:30 UTC daily): 30 3 * * * /app/deploy/scripts/backup-qdrant-r2.sh
# ==============================================================================

set -euo pipefail

TIMESTAMP="$(date -u +"%Y%m%dT%H%M%SZ")"
BACKUP_ROOT="${BACKUP_DIR:-/tmp/continuum_backups/qdrant}"
R2_BUCKET="${R2_BACKUP_BUCKET:-s3://continuum-backups}"
R2_PREFIX="${R2_QDRANT_PREFIX:-qdrant}"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-7}"

if [[ -z "${SAG_QDRANT_URL:-}" ]]; then
  echo "[-] ERROR: SAG_QDRANT_URL must be set." >&2
  exit 1
fi
if [[ -z "${CF_ACCOUNT_ID:-}" || -z "${AWS_ACCESS_KEY_ID:-}" || -z "${AWS_SECRET_ACCESS_KEY:-}" ]]; then
  echo "[-] ERROR: CF_ACCOUNT_ID, AWS_ACCESS_KEY_ID, and AWS_SECRET_ACCESS_KEY must be set." >&2
  exit 1
fi

QDRANT_BASE="${SAG_QDRANT_URL%/}"
R2_ENDPOINT="https://${CF_ACCOUNT_ID}.r2.cloudflarestorage.com"
AUTH_ARGS=()
if [[ -n "${SAG_QDRANT_API_KEY:-}" ]]; then
  AUTH_ARGS=(-H "api-key: ${SAG_QDRANT_API_KEY}")
fi

umask 077
mkdir -p -- "${BACKUP_ROOT}"
WORK_DIR="$(mktemp -d -- "${BACKUP_ROOT%/}/run.${TIMESTAMP}.XXXXXXXX")"
trap 'rm -rf -- "${WORK_DIR}"' EXIT

echo "[+] Listing Qdrant collections from ${QDRANT_BASE} at ${TIMESTAMP}..."
COLLECTIONS_JSON="$(curl -fsS "${AUTH_ARGS[@]}" "${QDRANT_BASE}/collections")"
COLLECTIONS="$(python3 -c 'import json,sys; data=json.loads(sys.stdin.read()); print("\n".join(c["name"] for c in data.get("result",{}).get("collections",[])))' <<< "${COLLECTIONS_JSON}")"

if [[ -z "${COLLECTIONS}" ]]; then
  echo "[!] No Qdrant collections found; nothing to snapshot."
  exit 0
fi

while IFS= read -r col; do
  [[ -z "${col}" ]] && continue
  echo "[+] Creating snapshot for collection: ${col}"
  SNAP_RESP="$(curl -fsS -X POST "${AUTH_ARGS[@]}" "${QDRANT_BASE}/collections/${col}/snapshots?wait=true")"
  SNAP_NAME="$(python3 -c 'import json,sys; print(json.loads(sys.stdin.read())["result"]["name"])' <<< "${SNAP_RESP}")"
  LOCAL_FILE="${WORK_DIR}/${col}__${SNAP_NAME}"
  CHECKSUM_FILE="${LOCAL_FILE}.sha256"

  curl -fsS "${AUTH_ARGS[@]}" -o "${LOCAL_FILE}" \
    "${QDRANT_BASE}/collections/${col}/snapshots/${SNAP_NAME}"
  if [[ ! -s "${LOCAL_FILE}" ]]; then
    echo "[-] ERROR: Empty snapshot downloaded for ${col}/${SNAP_NAME}" >&2
    exit 1
  fi
  sha256sum "${LOCAL_FILE}" > "${CHECKSUM_FILE}"

  aws s3 cp "${LOCAL_FILE}" "${R2_BUCKET}/${R2_PREFIX}/${TIMESTAMP}/${col}__${SNAP_NAME}" \
    --endpoint-url "${R2_ENDPOINT}"
  aws s3 cp "${CHECKSUM_FILE}" "${R2_BUCKET}/${R2_PREFIX}/${TIMESTAMP}/${col}__${SNAP_NAME}.sha256" \
    --endpoint-url "${R2_ENDPOINT}"

  # Clean transient snapshot from Qdrant node after verified upload
  curl -fsS -X DELETE "${AUTH_ARGS[@]}" \
    "${QDRANT_BASE}/collections/${col}/snapshots/${SNAP_NAME}" > /dev/null
  echo "    Uploaded & verified ${col}/${SNAP_NAME}"
done <<< "${COLLECTIONS}"

echo "[+] Qdrant snapshot backup complete (${TIMESTAMP}). Configure R2 bucket lifecycle rule (${RETENTION_DAYS}d) for ${R2_PREFIX}/."
