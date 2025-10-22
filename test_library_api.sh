#!/bin/bash

# Script de ejemplo para probar la API REST de Biblioteca usando curl
# Configura tu API_KEY antes de usar

# Configuración
BASE_URL="http://localhost:8069"
API_KEY="TU_API_KEY_AQUI"  # ⚠️ Reemplaza con tu API key real

echo "============================================================"
echo "🧪 PROBANDO API REST DE BIBLIOTECA CON CURL"
echo "============================================================"

# 1. Health Check
echo -e "\n1️⃣  Health Check..."
curl -s "${BASE_URL}/api/library/health" | jq '.' || echo "❌ Error"

# 2. Listar libros
echo -e "\n2️⃣  Listando primeros 5 libros..."
curl -s "${BASE_URL}/api/library/books?api_key=${API_KEY}&limit=5" | jq '.' || echo "❌ Error"

# 3. Buscar libros
echo -e "\n3️⃣  Buscando libros con 'Python'..."
curl -s "${BASE_URL}/api/library/books?api_key=${API_KEY}&search=Python" | jq '.' || echo "❌ Error"

# 4. Obtener detalle de un libro (ID 1)
echo -e "\n4️⃣  Detalle del libro ID 1..."
curl -s "${BASE_URL}/api/library/books/1?api_key=${API_KEY}" | jq '.' || echo "❌ Error"

# 5. Crear un libro
echo -e "\n5️⃣  Creando un nuevo libro..."
curl -X POST "${BASE_URL}/api/library/books" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "params": {
      "api_key": "'${API_KEY}'",
      "title": "JavaScript: The Good Parts",
      "isbn": "9780596517748",
      "sinopsis": "Un libro clásico sobre JavaScript",
      "copies": 2
    }
  }' | jq '.' || echo "❌ Error"

# 6. Listar miembros
echo -e "\n6️⃣  Listando miembros..."
curl -s "${BASE_URL}/api/library/members?api_key=${API_KEY}" | jq '.' || echo "❌ Error"

# 7. Listar préstamos activos
echo -e "\n7️⃣  Listando préstamos activos..."
curl -s "${BASE_URL}/api/library/loans?api_key=${API_KEY}&state=active" | jq '.' || echo "❌ Error"

# 8. Crear un préstamo (ejemplo comentado)
echo -e "\n8️⃣  Crear préstamo (ejemplo no ejecutado)..."
echo "# curl -X POST \"${BASE_URL}/api/library/loans\" \\"
echo "#   -H \"Content-Type: application/json\" \\"
echo "#   -d '{"
echo "#     \"jsonrpc\": \"2.0\","
echo "#     \"params\": {"
echo "#       \"api_key\": \"${API_KEY}\","
echo "#       \"member_id\": 5,"
echo "#       \"copy_id\": 2,"
echo "#       \"due_days\": 14,"
echo "#       \"auto_confirm\": true"
echo "#     }"
echo "#   }' | jq '.'"

# 9. Devolver un préstamo (ejemplo comentado)
echo -e "\n9️⃣  Devolver préstamo (ejemplo no ejecutado)..."
echo "# curl -X POST \"${BASE_URL}/api/library/loans/1/return\" \\"
echo "#   -H \"Content-Type: application/json\" \\"
echo "#   -d '{"
echo "#     \"jsonrpc\": \"2.0\","
echo "#     \"params\": {"
echo "#       \"api_key\": \"${API_KEY}\""
echo "#     }"
echo "#   }' | jq '.'"

echo -e "\n============================================================"
echo "✨ PRUEBAS COMPLETADAS"
echo "============================================================"
echo -e "\n💡 Tip: Genera tu API Key en Odoo:"
echo "   Ajustes → Usuarios → [Tu Usuario] → Pestaña 'API Access'"
echo "============================================================"
