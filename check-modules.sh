#!/bin/bash
# Script de utilidades para Odoo - Gestión de Módulos

set -e

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║       Odoo 18 - Gestión de Módulos                   ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""

# Función para contar módulos
count_modules() {
    echo -e "${YELLOW}📊 Contando módulos disponibles...${NC}"
    
    # Módulos base de Odoo (en el contenedor)
    BASE_COUNT=$(docker-compose exec odoo ls -1 /usr/lib/python3/dist-packages/odoo/addons 2>/dev/null | wc -l)
    
    # Módulos personalizados/enterprise
    EXTRA_COUNT=$(docker-compose exec odoo ls -1 /mnt/extra-addons 2>/dev/null | wc -l)
    
    # Total
    TOTAL=$((BASE_COUNT + EXTRA_COUNT))
    
    echo -e "${GREEN}✓${NC} Módulos base (Community): ${BASE_COUNT}"
    echo -e "${GREEN}✓${NC} Módulos adicionales (Enterprise + Personalizados): ${EXTRA_COUNT}"
    echo -e "${GREEN}✓${NC} Total de módulos disponibles: ${TOTAL}"
    echo ""
}

# Función para listar módulos personalizados
list_custom_modules() {
    echo -e "${YELLOW}📦 Módulos Personalizados:${NC}"
    docker-compose exec odoo ls -1 /mnt/extra-addons | grep -E "^(library_|mi_|custom_)" || echo "  Ninguno encontrado"
    echo ""
}

# Función para verificar módulos enterprise
check_enterprise() {
    echo -e "${YELLOW}💼 Verificando módulos Enterprise:${NC}"
    ENTERPRISE_MODULES=$(docker-compose exec odoo ls -1 /mnt/extra-addons 2>/dev/null | grep -E "^(account_|hr_|website_|sale_|stock_|purchase_)" | head -5)
    
    if [ -n "$ENTERPRISE_MODULES" ]; then
        echo -e "${GREEN}✓${NC} Módulos Enterprise detectados:"
        echo "$ENTERPRISE_MODULES" | while read module; do
            echo "  - $module"
        done
    else
        echo -e "${YELLOW}!${NC} No se detectaron módulos Enterprise"
    fi
    echo ""
}

# Función para mostrar la configuración de addons
show_config() {
    echo -e "${YELLOW}⚙️  Configuración de rutas de addons:${NC}"
    docker-compose exec odoo cat /etc/odoo/odoo.conf | grep "addons_path"
    echo ""
}

# Función para actualizar lista de módulos
update_module_list() {
    echo -e "${YELLOW}🔄 Actualizando lista de módulos en Odoo...${NC}"
    docker-compose exec odoo odoo -d odoo --stop-after-init --update=base --db_host=db --db_user=odoo --db_password=odoo 2>&1 | grep -E "(modules loaded|Registry loaded)" || true
    echo -e "${GREEN}✓${NC} Lista de módulos actualizada"
    echo ""
}

# Ejecutar todas las verificaciones
count_modules
check_enterprise
list_custom_modules
show_config

# Preguntar si quiere actualizar la lista de módulos
echo -e "${BLUE}¿Deseas actualizar la lista de módulos en Odoo? (s/n)${NC}"
read -r response
if [[ "$response" =~ ^[Ss]$ ]]; then
    update_module_list
fi

echo -e "${GREEN}✅ Verificación completada${NC}"
