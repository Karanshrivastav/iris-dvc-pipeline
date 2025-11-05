#!/usr/bin/env bash
set -euo pipefail

URL="$1"
CONCURRENCY="$2"
DURATION="${3:-30s}"
THREADS="${4:-4}"
OUTFILE="${5:-wrk-output.txt}"

echo "Running wrk against $URL (c=$CONCURRENCY, t=$THREADS, d=$DURATION)"
wrk -t"${THREADS}" -c"${CONCURRENCY}" -d"${DURATION}" -s ./scripts/wrk_post.lua "$URL" 2>&1 | tee "${OUTFILE}"

# Save some kubectl snapshots too (if k8s access present)
kubectl get pods -o wide > "${OUTFILE}.kubepods.txt" || true
kubectl top pods --no-headers >> "${OUTFILE}.kubepods.txt" || true
kubectl get hpa -o wide >> "${OUTFILE}.kubepods.txt" || true
