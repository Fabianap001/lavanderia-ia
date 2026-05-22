@echo off
echo Iniciando Analizador de Marquillas...

start "Python Service" cmd /k "cd python-service && uvicorn main:app --port 8000"
timeout /t 3
start "Node Backend" cmd /k "cd backend && node server.js"
timeout /t 2
start "" "frontend\index.html"

echo Listo! La aplicacion esta corriendo.