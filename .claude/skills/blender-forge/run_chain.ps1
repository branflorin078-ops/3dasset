# Build -> bake+export -> round-trip verify -> final card, through the lock runner.
# Usage (PowerShell 5.1):  .\run_chain.ps1 [outdir] [script]
#   defaults: outdir = .\out, script = examples\sunforged_greatsword.py
# Never call blender.exe directly: forge_run.py serialises every job machine-wide.
param(
    [string]$Out = (Join-Path $PSScriptRoot "out"),
    [string]$Script = (Join-Path $PSScriptRoot "examples\sunforged_greatsword.py")
)
New-Item -ItemType Directory -Force -Path $Out | Out-Null
$runner = Join-Path $PSScriptRoot "tools\forge_run.py"
$t0 = Get-Date
py $runner chain $Script $Out
$code = $LASTEXITCODE
"chain: exit $code after $([int]((Get-Date) - $t0).TotalSeconds) s"
# The two lines that prove the delivery: the export gates and the file the verify step opened.
Get-ChildItem -Path $Out -Filter *.log | Select-String -Pattern '^QA_GAME|^IMPORT' | ForEach-Object { $_.Line }
exit $code
