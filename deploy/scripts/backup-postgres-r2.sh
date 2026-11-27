#!/usr/bin/env bash
# ==============================================================================
# Continuum AI — Automated SAG PostgreSQL 16 Backup to Cloudflare R2
# Dumps the authoritative `sag` metadata, ACL, document versions, and knowledge
# graph tables using custom compressed pg_dump with SHA-256 verification and
# 7-day retention pruning.
#
# Cron (03:15 UTC daily): 15 3 * * * /app/deploy/scripts/backup-postgres-r2.sh
# ==============================================================================

set -euo pipefail

TIMESTAMP="$(date -u +"%Y%m%dT%H%M%SZ")"
BACKUP_DIR="${BACKUP_DIR:-/tmp/continuum_backups/postgres}"
BACKUP_PREFIX="continuum_sag_pg16"
BACKUP_FILE="${BACKUP_DIR}/${BACKUP_PREFIX}_${TIMESTAMP}.dump"
CHECKSUM_FILE="${BACKUP_FILE}.sha256"
R2_BUCKET="${R2_BACKUP_BUCKET:-s3://continuum-backups}"
R2_PREFIX="${R2_POSTGRES_PREFIX:-postgres}"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-7}"

PG_BACKUP_DSN="${SAG_PG_BACKUP_DSN:-${SAG_DATABASE_URL:-}}"
if [[ "${PG_BACKUP_DSN}" == postgresql+asyncpg://* ]]; then
  PG_BACKUP_DSN="postgresql://${PG_BACKUP_DSN#postgresql+asyncpg://}"
fi
if [[ "${PG_BACKUP_DSN}" != postgresql://* && "${PG_BACKUP_DSN}" != postgres://* ]]; then
  echo "[-] ERROR: Set SAG_PG_BACKUP_DSN or SAG_DATABASE_URL to a PostgreSQL URI." >&2
  exit 1
fi
if [[ -z "${CF_ACCOUNT_ID:-}" || -z "${AWS_ACCESS_KEY_ID:-}" || -z "${AWS_SECRET_ACCESS_KEY:-}" ]]; then
  echo "[-] ERROR: CF_ACCOUNT_ID, AWS_ACCESS_KEY_ID, and AWS_SECRET_ACCESS_KEY must be set." >&2
  exit 1
fi

R2_ENDPOINT="https://${CF_ACCOUNT_ID}.r2.cloudflarestorage.com"
mkdir -p "${BACKUP_DIR}"
trap 'rm -f "${BACKUP_FILE}" "${CHECKSUM_FILE}"' EXIT

echo "[+] Starting SAG PostgreSQL 16 backup at ${TIMESTAMP}..."
pg_dump \
  --dbname="${PG_BACKUP_DSN}" \
  --format=custom \
  --compress=9 \
  --no-owner \
  --no-privileges \
  --file="${BACKUP_FILE}"

if [[ ! -s "${BACKUP_FILE}" ]]; then
  echo "[-] ERROR: PostgreSQL dump file is empty or missing." >&2
  exit 1
fi

# Verify custom-format archive TOC cleanly before upload
pg_restore --list "${BACKUP_FILE}" > /dev/null
sha256sum "${BACKUP_FILE}" > "${CHECKSUM_FILE}"
echo "[+] PG16 dump verified: $(du -sh "${BACKUP_FILE}" | cut -f1) | SHA-256: $(cut -d' ' -f1 "${CHECKSUM_FILE}")"

echo "[+] Uploading dump and SHA-256 checksum to ${R2_BUCKET}/${R2_PREFIX}/..."
aws s3 cp "${BACKUP_FILE}" "${R2_BUCKET}/${R2_PREFIX}/${BACKUP_PREFIX}_${TIMESTAMP}.dump" \
  --endpoint-url "${R2_ENDPOINT}"
aws s3 cp "${CHECKSUM_FILE}" "${R2_BUCKET}/${R2_PREFIX}/${BACKUP_PREFIX}_${TIMESTAMP}.dump.sha256" \
  --endpoint-url "${R2_ENDPOINT}"

echo "[+] Pruning R2 PostgreSQL backups older than ${RETENTION_DAYS} days..."
CUTOFF_EPOCH="$(date -u -d "${RETENTION_DAYS} days ago" +%s 2>/dev/null || python3 -c "import time; print(int(time.time() - ${RETENTION_DAYS} * 86400))")"
aws s3 ls "${R2_BUCKET}/${R2_PREFIX}/" --endpoint-url "${R2_ENDPOINT}" | while read -r fdate ftime _fsize fname; do
  [[ -z "${fname:-}" ]] && continue
  file_epoch="$(date -u -d "${fdate} ${ftime}" +%s 2>/dev/null || true)"
  if [[ -n "${file_epoch}" && "${file_epoch}" -lt "${CUTOFF_EPOCH}" ]]; then
    echo "    Pruning expired object: ${fname}"
    aws s3 rm "${R2_BUCKET}/${R2_PREFIX}/${fname}" --endpoint-url "${R2_ENDPOINT}"
  fi
done

echo "[+] SAG PostgreSQL 16 backup complete (${TIMESTAMP})."
