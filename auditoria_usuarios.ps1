# auditoria_usuarios.ps1
# Script para auditar usuarios locales


# Obtener todos los usuarios locales
$usuarios = Get-LocalUser

# Arreglos para clasificar
$sinLogon = @()
$conLogon = @()

# Recorrer cada usuario
foreach ($u in $usuarios) {
    if (-not $u.LastLogon) {
        # Nunca inició sesión
        $sinLogon += "$($u.Name): Estado = $($u.Enabled), Último acceso = NUNCA"
    } else {
        # Sí inició sesión
        $conLogon += "$($u.Name): Estado = $($u.Enabled), Último acceso = $($u.LastLogon)"
    }
}

# Rutas de archivos
$desktop = "$env:USERPROFILE\OneDrive\Escritorio"
$archivoSin = "$desktop\usuarios_sin_logon.txt"
$archivoCon = "$desktop\usuarios_con_logon.txt"
$reporte    = "$desktop\reporte_usuarios.txt"

# Limpiar archivos antes de escribir
"" > $archivoSin
"" > $archivoCon
"" > $reporte

# Guardar en archivos separados 
$sinLogon | ForEach-Object { $_ >> $archivoSin }
$conLogon | ForEach-Object { $_ >> $archivoCon }

# Crear reporte combinado
"==== REPORTE DE USUARIOS ====" >> $reporte
"`n Usuarios que NUNCA han iniciado sesión:" >> $reporte
$sinLogon | ForEach-Object { $_ >> $reporte }
"`n Usuarios que SÍ han iniciado sesión:" >> $reporte
$conLogon | ForEach-Object { $_ >> $reporte }

# Mostrar en pantalla
Write-Output "`n ==== RESUMEN DE AUDITORÍA ===="
Write-Output "`n Usuarios que NUNCA han iniciado sesión:"
$sinLogon | ForEach-Object { Write-Output $_ }
Write-Output "`n Usuarios que SÍ han iniciado sesión:"
$conLogon | ForEach-Object { Write-Output $_ }
Write-Output "`n Archivos generados en el Escritorio:"
Write-Output " - usuarios_sin_logon.txt"
Write-Output " - usuarios_con_logon.txt"
Write-Output " - reporte_usuarios.txt"
