#!/usr/bin/env bash
# ==============================================================================
# Continuum AI — Script Tự Động Sao Lưu MongoDB Lên Cloudflare R2 (Chi phí 0 VNĐ)
# Đặt cronjob chạy lúc 03:00 AM mỗi ngày: 0 3 * * * /app/deploy/scripts/backup-mongodb-r2.sh
# ==============================================================================

set -euo pipefail

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/tmp/continuum_backups"
BACKUP_FILE="${BACKUP_DIR}/continuum_db_${TIMESTAMP}.gz"
R2_BUCKET="s3://continuum-backups"

# Kiểm tra các biến môi trường Cloudflare R2
if [ -z "${CF_ACCOUNT_ID:-}" ] || [ -z "${AWS_ACCESS_KEY_ID:-}" ] || [ -z "${AWS_SECRET_ACCESS_KEY:-}" ]; then
  echo "[-] Lỗi: Chưa thiết lập biến môi trường CF_ACCOUNT_ID, AWS_ACCESS_KEY_ID hoặc AWS_SECRET_ACCESS_KEY."
  exit 1
fi

mkdir -p "${BACKUP_DIR}"

echo "[+] Bắt đầu tạo bản sao lưu MongoDB tại ${TIMESTAMP}..."
mongodump \
  --uri="${MONGODB_URI:-mongodb://localhost:27017/continuum?replicaSet=rs0}" \
  --archive="${BACKUP_FILE}" \
  --gzip

echo "[+] Bản sao lưu cục bộ đã tạo: $(du -sh "${BACKUP_FILE}" | cut -f1)"

echo "[+] Đang tải lên Cloudflare R2 (Endpoint: https://${CF_ACCOUNT_ID}.r2.cloudflarestorage.com)..."
aws s3 cp "${BACKUP_FILE}" "${R2_BUCKET}/continuum_db_${TIMESTAMP}.gz" \
  --endpoint-url "https://${CF_ACCOUNT_ID}.r2.cloudflarestorage.com"

echo "[+] Xoá tệp tạm thời trên ổ cứng VPS..."
rm -f "${BACKUP_FILE}"

echo "[+] Hoàn tất sao lưu an toàn lên Cloudflare R2!"
