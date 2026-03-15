# Prende il controllo del buffer visivo del terminale
$Host.UI.RawUI.BackgroundColor = "Black"
$Host.UI.RawUI.ForegroundColor = "Green"
Clear-Host

Write-Host "[*] Inizializzazione diagnostica di sistema in memoria..." -ForegroundColor DarkGreen
Start-Sleep -Seconds 1

# Interroga il kernel per i metadati hardware tramite il Common Information Model (CIM)
$os = Get-CimInstance Win32_OperatingSystem
$cpu = Get-CimInstance Win32_Processor
$gpu = Get-CimInstance Win32_VideoController

Write-Host "`n[+] Estrazione Dati Completata:" -ForegroundColor Cyan
Write-Host "    OS: $($os.Caption) ($($os.OSArchitecture))"
Write-Host "    CPU: $($cpu.Name)"
Write-Host "    GPU: $($gpu.Name)"
Write-Host "    RAM Libera: $([math]::Round($os.FreePhysicalMemory/1024, 2)) MB"

# Blocca il thread per impedire l'autochiusura del processo
Write-Host "`n[!] Premi un tasto qualsiasi per distruggere l'istanza..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")