# Revisa lo pendiente de <PROYECTO> con el agente revisor de OpenCode y guarda el informe con fecha.
# Uso:  .\revisar-pendiente.ps1                 → lo que hay sin commitear
#       .\revisar-pendiente.ps1 -Rama main      → la rama actual contra main
# Lánzalo desde el repo (o con -Repo). Si el modelo es local, con su servidor arrancado. No toca nada: el revisor no puede editar.
param(
    [string]$Repo = (Get-Location).Path,
    [string]$Rama = '',
    # RELLENAR: las extensiones de código del proyecto y lo que no se revisa (generado, minificado…)
    [string]$Extensiones = 'py|js|ts|html|css',
    [string]$Excluir = '\.min\.|node_modules/'
)

$informes = Join-Path $PSScriptRoot '..\informes'
New-Item -ItemType Directory -Force $informes | Out-Null
Set-Location $Repo

# Sin cambios de código no merece la pena despertar al modelo
$cambios = if ($Rama) { git diff --name-only "$Rama...HEAD" 2>$null } else { @(git diff --name-only HEAD 2>$null) + @(git ls-files --others --exclude-standard 2>$null) }
$codigo = @($cambios | Where-Object { $_ -match "\.($Extensiones)$" -and $_ -notmatch $Excluir })
if (-not $codigo) {
    Write-Host 'Nada de código pendiente que revisar.'
    exit 0
}
Write-Host ("Revisando {0} ficheros con el revisor..." -f $codigo.Count)

$alcance = if ($Rama) { "la rama actual contra $Rama (git diff $Rama...HEAD)" } else { 'lo pendiente sin commitear' }
$pedido = "Revisa $alcance siguiendo tu método completo y termina con el veredicto. Ficheros: $($codigo -join ', ')"
$fecha = Get-Date -Format 'yyyy-MM-dd_HHmm'
$informe = Join-Path $informes "revision_$fecha.md"

$reloj = [Diagnostics.Stopwatch]::StartNew()
$salida = opencode run --agent revisor --title "revisión $fecha" $pedido 2>$null
$reloj.Stop()

@("# Revisión $fecha", '', "Alcance: $alcance · $($codigo.Count) ficheros · $([int]$reloj.Elapsed.TotalMinutes) min $($reloj.Elapsed.Seconds) s", '') + $salida |
    Set-Content -Path $informe -Encoding utf8
Write-Host "Informe: $informe"
