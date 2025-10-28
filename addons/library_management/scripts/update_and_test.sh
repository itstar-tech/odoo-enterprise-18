#!/bin/bash

if [ -z "$1" ]; then
    echo "❌ Error: Debes especificar el nombre de la base de datos"
    echo ""
    echo "Uso: $0 NOMBRE_BASE_DATOS"
    echo ""
    echo "Bases de datos disponibles:"
    psql -l 2>/dev/null | grep -E "^\s+\w+" | awk '{print "  - " $1}' | grep -v "template" | grep -v "postgres" | head -10
    exit 1
fi

DB_NAME="$1"

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║     ACTUALIZAR Y PROBAR - Módulo Biblioteca                  ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Base de datos: $DB_NAME"
echo ""

echo "⏳ Paso 1: Actualizando módulo library_management..."
echo ""

odoo-bin -u library_management -d "$DB_NAME" --stop-after-init --log-level=warn 2>&1 | grep -E "(Modules loaded|library_management|Upgrading|Error|WARNING)" | tail -20

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo ""
    echo "✅ Módulo actualizado correctamente"
else
    echo ""
    echo "❌ Error al actualizar el módulo"
    exit 1
fi

echo ""
echo "⏳ Paso 2: Verificando que Odoo esté corriendo..."
echo ""

if curl -s http://localhost:8069/web/database/selector 2>&1 | grep -q "odoo"; then
    echo "✅ Odoo está corriendo"
else
    echo "❌ Odoo no está corriendo"
    echo ""
    echo "Inicia Odoo con:"
    echo "  odoo-bin -d $DB_NAME"
    echo ""
    echo "Luego ejecuta este script nuevamente"
    exit 1
fi

echo ""
echo "⏳ Paso 3: Probando API Key..."
echo ""

cd /home/luna/Documents/code/odoo/addons/library_management
python3 scripts/test_my_api_key.py

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                    PROCESO COMPLETADO                         ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
