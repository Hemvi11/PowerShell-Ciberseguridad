function Validar-Archivo {
    param (
        [string]$Ruta
    )
    try {
        if (Test-Path $Ruta) {
            $contenido = Get-Content $Ruta -ErrorAction Stop
            $resultado = "Archivo encontrado y accesible: $Ruta"
        } else {
            throw "El archivo no existe."
        }
    }
    catch {
        $resultado = "Error: $_"
    }
    finally {
        Write-Host "Validación finalizada para: $Ruta" -ForegroundColor Cyan
    }

    return $resultado
}

# ---------------------------
# Sección principal del script
# ---------------------------

# Lista de archivos críticos a validar
$archivos = @(
    "$env:USERPROFILE\OneDrive\Escritorio\archivo.txt",   # Archivo de prueba
    "C:\Windows\System32\drivers\etc\hosts"   # Ejemplo de archivo crítico
)

# Generar nombre dinámico para el reporte
$fecha = Get-Date -Format "ddMMyyyy"
$reporte = "$PSScriptRoot\Evidencia10_reporte_$fecha.txt"

# Crear o sobrescribir reporte
"==== REPORTE DE VALIDACION DE ARCHIVOS ====" | Out-File -FilePath $reporte

foreach ($archivo in $archivos) {
    $resultado = Validar-Archivo -Ruta $archivo
    $resultado | Tee-Object -FilePath $reporte -Append
}

"==== Validacion completada el $(Get-Date) ====" | Out-File -FilePath $reporte -Append