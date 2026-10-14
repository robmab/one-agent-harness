# Reviews what's pending in <PROJECT> with OpenCode's reviewer agent and saves a dated report.
# Usage:  .\review-pending.ps1                  -> what's uncommitted
#         .\review-pending.ps1 -Branch main     -> the current branch against main
# Run it from the repo (or with -Repo). If the model is local, with its server running. It touches nothing: the reviewer can't edit.
# ASCII only on purpose: Windows PowerShell 5.1 misreads UTF-8 scripts without a BOM.
param(
    [string]$Repo = (Get-Location).Path,
    [string]$Branch = '',
    # FILL-IN: the project's code extensions and what isn't reviewed (generated, minified...)
    [string]$Extensions = 'py|js|ts|html|css',
    [string]$Exclude = '\.min\.|node_modules/'
)

$reports = Join-Path $PSScriptRoot '..\reports'
New-Item -ItemType Directory -Force $reports | Out-Null
Set-Location $Repo

# No code changes, no point waking the model up
$changes = if ($Branch) { git diff --name-only "$Branch...HEAD" 2>$null } else { @(git diff --name-only HEAD 2>$null) + @(git ls-files --others --exclude-standard 2>$null) }
$code = @($changes | Where-Object { $_ -match "\.($Extensions)$" -and $_ -notmatch $Exclude })
if (-not $code) {
    Write-Host 'No pending code to review.'
    exit 0
}
Write-Host ("Reviewing {0} files with the reviewer..." -f $code.Count)

$scope = if ($Branch) { "the current branch against $Branch (git diff $Branch...HEAD)" } else { 'what is pending and uncommitted' }
$request = "Review $scope following your full method and finish with the verdict. Files: $($code -join ', ')"
$date = Get-Date -Format 'yyyy-MM-dd_HHmm'
$report = Join-Path $reports "review_$date.md"

$clock = [Diagnostics.Stopwatch]::StartNew()
$output = opencode run --agent reviewer --title "review $date" $request 2>$null
$clock.Stop()

@("# Review $date", '', "Scope: $scope - $($code.Count) files - $([int]$clock.Elapsed.TotalMinutes) min $($clock.Elapsed.Seconds) s", '') + $output |
    Set-Content -Path $report -Encoding utf8
Write-Host "Report: $report"
