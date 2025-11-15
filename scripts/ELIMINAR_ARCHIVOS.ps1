# Script para eliminar archivos innecesarios del proyecto
# Ejecutar con: .\ELIMINAR_ARCHIVOS.ps1

Write-Host "🗑️  LIMPIANDO ARCHIVOS INNECESARIOS..." -ForegroundColor Yellow
Write-Host ""

# Lista de archivos a eliminar
$archivos_eliminar = @(
    # Tests
    "test_connector.py",
    "test_consulta.py",
    "test_crear_usuario.py",
    "test_main.py",
    "test_real_system.py",
    "tests.py",
    "verificar_databases.py",
    
    # Diagnóstico
    "ver_barrios_real.py",
    "ver_barrios.py",
    "ver_ciudades.py",
    "ver_tipos.py",
    
    # Documentación extra (conservar solo 1 README si quieres)
    "COMO_HACER_CLICKS.md",
    "COMO_USAR.md",
    "GUIA_USO.md",
    "INSTALL_NEO4J.md",
    "README_NUEVO.md",
    
    # Sistemas alternativos
    "main_backup.py",
    "conversational_ai.py",
    "real_system_with_neo4j.py",
    "recommendation_system.py",
    "red_marcos_sistema_recomendacion.py",
    "recommendation_engine.py",
    
    # Scripts específicos opcionales
    "migrate_to_neo4j.py",
    "populate_real_data.py",
    "sample_data.py",
    "cypher_queries.py"
)

$contador = 0
$errores = 0

foreach ($archivo in $archivos_eliminar) {
    if (Test-Path $archivo) {
        try {
            Remove-Item $archivo -Force
            Write-Host "✅ Eliminado: $archivo" -ForegroundColor Green
            $contador++
        }
        catch {
            Write-Host "❌ Error eliminando: $archivo" -ForegroundColor Red
            $errores++
        }
    }
    else {
        Write-Host "⚠️  No existe: $archivo" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "📊 RESUMEN:" -ForegroundColor Cyan
Write-Host "   ✅ Archivos eliminados: $contador" -ForegroundColor Green
Write-Host "   ⚠️  Archivos no encontrados: $($archivos_eliminar.Count - $contador - $errores)" -ForegroundColor Yellow
Write-Host "   ❌ Errores: $errores" -ForegroundColor Red
Write-Host ""
Write-Host "✨ LIMPIEZA COMPLETADA" -ForegroundColor Green
