#!/bin/bash
# Memory-capped edep-sim run. Usage: run_edepsim.sh [-m 6G] [-t 1800] <edep-sim args...>
# Runs inside a cgroup scope (MemoryMax, no swap) with a wall-clock timeout,
# so a runaway event is OOM-killed inside the scope instead of taking down the machine.
MEM=6G; TMO=1800
while true; do
  case "$1" in -m) MEM=$2; shift 2;; -t) TMO=$2; shift 2;; *) break;; esac
done
LARTPC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
eval "$(pixi shell-hook --manifest-path "$LARTPC_DIR/pixi.toml")"
source "$LARTPC_DIR/env.sh"
exec systemd-run --user --scope --quiet -p MemoryMax=$MEM -p MemorySwapMax=0 \
  timeout $TMO edep-sim "$@"
