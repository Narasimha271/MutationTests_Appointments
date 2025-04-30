@echo off
docker build --no-cache -t mutation-test .
docker run --rm -v "%cd%:/app" mutation-test
pause
