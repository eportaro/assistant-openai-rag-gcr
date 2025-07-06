# 📋 COMANDOS GITHUB — Guía rápida

Este archivo contiene una lista secuencial de comandos esenciales para trabajar con GitHub desde tu entorno local (incluyendo contenedores Docker como en VS Code).

| Nº  | Comando                                                                 | Descripción                                                              |
|-----|-------------------------------------------------------------------------|---------------------------------------------------------------------------|
| 1   | `pwd`                                                                   | Verifica la ruta actual del proyecto (útil en contenedor o terminal)     |
| 2   | `ls -la`                                                                | Lista todos los archivos del proyecto, incluidos ocultos (`.git`, etc.)  |
| 3   | `rm -rf .git`                                                           | Elimina el repositorio Git local (si hubo errores previos)               |
| 4   | `git init`                                                              | Inicializa un repositorio Git en el directorio local                     |
| 5   | `git config --global user.name "Eduardo Portaro"`                      | Configura tu nombre como autor de los commits                            |
| 6   | `git config --global user.email "eportaro@gmail.com"`                  | Configura tu correo como autor                                           |
| 7   | `git config --global init.defaultBranch main`                          | Define "main" como rama inicial (por defecto es "master")                |
| 8   | `echo "src/.env" >> .gitignore`                                        | Agrega archivo `.env` al `.gitignore` para no subirlo a GitHub           |
| 9   | `echo "src/project-asistente-openai-eapr-*.json" >> .gitignore`       | Ignora archivos de credenciales de Google Cloud                          |
| 10  | `git add .`                                                             | Agrega todos los archivos al staging (lista de archivos a guardar)       |
| 11  | `git status`                                                            | Muestra qué archivos están listos para el commit                         |
| 12  | `git commit -m "Primer commit limpio sin secretos"`                   | Crea el primer snapshot (commit) del proyecto                            |
| 13  | `git remote add origin https://github.com/eportaro/assistant-openai-rag-gcr.git` | Vincula tu repositorio local al remoto en GitHub              |
| 14  | `git remote -v`                                                         | Verifica que el repositorio esté bien conectado a GitHub                 |
| 15  | `git pull origin main --rebase`                                        | Trae archivos remotos si GitHub ya tiene contenido (como README)         |
| 16  | `git push -u origin main`                                              | Sube los archivos a tu repositorio GitHub                                |
| 17  | `git log --oneline`                                                    | Muestra un resumen de los commits                                        |
| 18  | `git diff`                                                              | Muestra diferencias entre el estado actual y el último commit            |
| 19  | `git reset --hard`                                                     | Borra todos los cambios no guardados (¡cuidado!)                         |
| 20  | `git checkout .`                                                       | Restaura los archivos al último commit sin borrarlos del disco           |
