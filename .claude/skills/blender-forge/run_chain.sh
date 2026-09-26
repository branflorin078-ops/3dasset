#!/bin/sh
# Build → bake+export → round-trip verify → final card, chained (safe on 1 CPU core).
# Usage: ./run_chain.sh [outdir]        (requires `blender` 4.0+ on PATH)
HERE="$(cd "$(dirname "$0")" && pwd)"; OUT="${1:-$HERE/out}"; mkdir -p "$OUT"
cd "$HERE/examples"
run() { s=$(date +%s); timeout "$1" blender --background --python "$2" -- $3 > "$OUT/$4.log" 2>&1
        echo "$4: exit $? after $(( $(date +%s)-s ))s"; }
run 2400 sunforged_greatsword.py "export $OUT" export
run 1200 verify_glb.py "verify $OUT" verify
run 3000 sunforged_greatsword.py "final $OUT" final
grep -h "^QA_GAME\|^IMPORT" "$OUT"/export.log "$OUT"/verify.log
