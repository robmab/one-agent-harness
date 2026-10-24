# Revisa lo pendiente de <PROJECT> con el agente revisor de OpenCode y guarda el informe con fecha.
# Uso:  .\review-pending.ps1                  -> lo que hay sin commitear
#       .\review-pending.ps1 -Branch main     -> la rama actual contra main
# Lanzalo desde el repo (o con -Repo). Si el modelo es local, con su servidor arrancado. No toca nada: el revisor no puede editar.
# Solo ASCII a proposito (sin tildes): Windows PowerShell 5.1 lee mal los scripts UTF-8 sin BOM.
param(
    [string]$Repo = (Get-Location).Path,
    [string]$Branch = '',
    # FILL-IN: las extensiones de codigo del proyecto y lo que no se revisa (generado, minificado...)
    [string]$Extensions = 'py|js|ts|html|css',
    [string]$Exclude = '\.min\.|node_modules/'
)

$reports = Join-Path (Split-Path $PSScriptRoot) 'reports'
New-Item -ItemType Directory -Force $reports | Out-Null
Set-Location $Repo

# Sin cambios de codigo no merece la pena despertar al modelo
$changes = if ($Branch) { git diff --name-only "$Branch...HEAD" 2>$null } else { @(git diff --name-only HEAD 2>$null) + @(git ls-files --others --exclude-standard 2>$null) }
$code = @($changes | Where-Object { $_ -match "\.($Extensions)$" -and $_ -notmatch $Exclude })
if (-not $code) {
    Write-Host 'Nada de codigo pendiente que revisar.'
    exit 0
}
Write-Host ("Revisando {0} ficheros con el revisor..." -f $code.Count)

$scope = if ($Branch) { "la rama actual contra $Branch (git diff $Branch...HEAD)" } else { 'lo pendiente sin commitear' }
$request = "Revisa $scope siguiendo tu metodo completo y termina con el veredicto. Ficheros: $($code -join ', ')"
$date = Get-Date -Format 'yyyy-MM-dd_HHmm'
$report = Join-Path $reports "revision_$date.md"

$clock = [Diagnostics.Stopwatch]::StartNew()
$output = opencode run --agent reviewer --title "revision $date" $request 2>$null
$clock.Stop()

@("# Revision $date", '', "Alcance: $scope - $($code.Count) ficheros - $([int]$clock.Elapsed.TotalMinutes) min $($clock.Elapsed.Seconds) s", '') + $output |
    Set-Content -Path $report -Encoding utf8
Write-Host "Informe: $report"
