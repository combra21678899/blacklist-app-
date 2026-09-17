# Informe de Pruebas de Integración — Blacklist API

**Asignatura:** Electiva IV — Clase 2502  
**Docente:** Ronald Carrascal Carreazo  
**Institución:** Fundación Universitaria Tecnológico Comfenalco  
**Programa:** Ingeniería de Sistemas  
**Fecha:** Septiembre 2026  

**Integrantes:**
- Carlos Villamil
- Isabella Sofía
- Liannys Sophia

**Repositorio:** [https://github.com/combra21678899/blacklist-app-](https://github.com/combra21678899/blacklist-app-)

---

## 1. Crear colección en Postman de las capacidades del servicio `blacklist_email`

Se creó una colección llamada **Blacklist API** con las 4 peticiones que representan las capacidades del servicio:

| # | Nombre | Método | Endpoint | Requiere Token |
|---|--------|--------|----------|---------------|
| 1 | Ping | GET | `/blacklists/ping` | ❌ |
| 2 | Health | GET | `/health` | ❌ |
| 3 | Create Blacklist | POST | `/blacklists` | ✅ |
| 4 | Check Blacklist | GET | `/blacklists/{{email}}` | ✅ |

Cada petición incluye **scripts de aserción** para validar el código de estado y el contenido de la respuesta.

---

## 2. Exportar `.json` de la colección generada

La colección se exportó en formato **Collection v2.1** con el nombre: blacklist-api.postman_collection.json


Este archivo se incluyó en la **raíz del repositorio** para ser usado posteriormente por Newman.

**Enlace al archivo exportado:**  
[blacklist-api.postman_collection.json](https://github.com/combra21678899/blacklist-app-/blob/main/blacklist-api.postman_collection.json)

---

## 3. Ejecutar Newman de manera local para probar la colección

Se instaló Newman globalmente:

```bash
npm install -g newman


newman run blacklist-api.postman_collection.json \
  --env-var baseUrl=http://localhost:5001 \
  --env-var token=dev-token-12345

Fragmento del workflow:

pruebas_integracion:
  runs-on: ubuntu-latest
  needs: test
  steps:
    - uses: actions/checkout@v4
    - name: Crear archivo .env para CI
      run: |
        echo "DATABASE_URL=postgresql://postgres:postgres@db:5432/blacklist_db" > .env
        echo "BEARER_TOKEN=dev-token-12345" >> .env
        echo "FLASK_ENV=development" >> .env
        echo "FLASK_APP=src.main" >> .env
        echo "PORT=5000" >> .env
    - name: Levantar servicios con Docker Compose
      run: docker compose up -d --build
    - name: Esperar a que la app este lista
      run: |
        for i in {1..30}; do
          if curl -s http://localhost:5001/blacklists/ping | grep -q pong; then
            exit 0
          fi
          sleep 2
        done
        exit 1
    - uses: actions/setup-node@v4
      with:
        node-version: '20'
    - run: npm install -g newman
    - run: |
        newman run blacklist-api.postman_collection.json \
          --env-var baseUrl=http://localhost:5001 \
          --env-var token=dev-token-12345
    - if: always()
      run: docker compose down



