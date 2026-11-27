#!/usr/bin/env bash
# ==============================================================================
# Continuum AI — Automated Full-Instance MongoDB Backup to Cloudflare R2
# Covers ALL database-per-service DBs (continuum_iam, continuum_capture,
# continuum_task, continuum_handover, continuum_chat, continuum_notification,
# continuum_audit, continuum_jira, continuum_ingestion, continuum_lifecycle)
# with point-in-time --oplog consistency, SHA-256 verification, and 7-day pruning.
#
# Cron (03:00 UTC daily): 0 3 * * * /app/deploy/scripts/backup-mongodb-r2.sh
# ==============================================================================

set -euo pipefail

TIMESTAMP="$(date -u +"%Y%m%dT%H%M%SZ")"
BACKUP_DIR="${BACKUP_DIR:-/tmp/continuum_backups/mongodb}"
BACKUP_PREFIX="continuum_mongodb_full"
BACKUP_FILE="${BACKUP_DIR}/${BACKUP_PREFIX}_${TIMESTAMP}.archive.gz"
CHECKSUM_FILE="${BACKUP_FILE}.sha256"
R2_BUCKET="${R2_BACKUP_BUCKET:-s3://continuum-backups}"
R2_PREFIX="${R2_MONGODB_PREFIX:-mongodb}"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-7}"

# Full-instance URI MUST NOT include a single database path suffix (e.g. /continuum),
# otherwise mongodump skips all 10 database-per-service databases!
MONGODB_BACKUP_URI="${MONGODB_URI:-mongodb://localhost:27017/?replicaSet=rs0}"
if [[ "${MONGODB_BACKUP_URI}" =~ ^mongodb(\+srv)?://[^/]+/[^?]+ ]]; then
  echo "[-] ERROR: MONGODB_URI specifies a single database path; strip the /<db> suffix to dump all service databases." >&2
  exit 1
fi

if [[ -z "${CF_ACCOUNT_ID:-}" || -z "${AWS_ACCESS_KEY_ID:-}" || -z "${AWS_SECRET_ACCESS_KEY:-}" ]]; then
  echo "[-] ERROR: CF_ACCOUNT_ID, AWS_ACCESS_KEY_ID, and AWS_SECRET_ACCESS_KEY must be set." >&2
  exit 1
fi

R2_ENDPOINT="https://${CF_ACCOUNT_ID}.r2.cloudflarestorage.com"
mkdir -p "${BACKUP_DIR}"
trap 'rm -f "${BACKUP_FILE}" "${CHECKSUM_FILE}"' EXIT

echo "[+] Starting full-instance MongoDB backup (--oplog) at ${TIMESTAMP}..."
mongodump \
  --uri="${MONGODB_BACKUP_URI}" \
  --oplog \
  --archive="${BACKUP_FILE}" \
  --gzip

if [[ ! -s "${BACKUP_FILE}" ]]; then
  echo "[-] ERROR: Backup archive is empty or missing." >&2
  exit 1
fi

sha256sum "${BACKUP_FILE}" > "${CHECKSUM_FILE}"
echo "[+] Archive created: $(du -sh "${BACKUP_FILE}" | cut -f1) | SHA-256: $(cut -d' ' -f1 "${CHECKSUM_FILE}")"

# Optional archive integrity verification (lists TOC via gzip -t)
gzip -t "${BACKUP_FILE}"
echo "[+] Gzip integrity check passed."

echo "[+] Uploading archive and SHA-256 checksum to ${R2_BUCKET}/${R2_PREFIX}/..."
aws s3 cp "${BACKUP_FILE}" "${R2_BUCKET}/${R2_PREFIX}/${BACKUP_PREFIX}_${TIMESTAMP}.archive.gz" \
  --endpoint-url "${R2_ENDPOINT}"
aws s3 cp "${CHECKSUM_FILE}" "${R2_BUCKET}/${R2_PREFIX}/${BACKUP_PREFIX}_${TIMESTAMP}.archive.gz.sha256" \
  --endpoint-url "${R2_ENDPOINT}"

echo "[+] Pruning R2 backups older than ${RETENTION_DAYS} days..."
CUTOFF_EPOCH="$(date -u -d "${RETENTION_DAYS} days ago" +%s 2>/dev/null || python3 -c "import time; print(int(time.time() - ${RETENTION_DAYS} * 86400))")"
aws s3 ls "${R2_BUCKET}/${R2_PREFIX}/" --endpoint-url "${R2_ENDPOINT}" | while read -r fdate ftime _fsize fname; do
  [[ -z "${fname:-}" ]] && continue
  file_epoch="$(date -u -d "${fdate} ${ftime}" +%s 2>/dev/null || true)"
  if [[ -n "${file_epoch}" && "${file_epoch}" -lt "${CUTOFF_EPOCH}" ]]; then
    echo "    Pruning expired object: ${fname}"
    aws s3 rm "${R2_BUCKET}/${R2_PREFIX}/${fname}" --endpoint-url "${R2_ENDPOINT}"
  fi
done

echo "[+] MongoDB full-instance backup complete (${TIMESTAMP})."
