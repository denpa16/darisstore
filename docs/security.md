# БЕЗОПАСТНОСТЬ

## Современный интерент стал опастной штукой

<img src="https://media.giphy.com/media/LpkLWXTp0v0qy70xPp/giphy.gif">

## Но с помощью современных решений мы сделаем себе жизнь чуточку лучше

<img src="https://media.giphy.com/media/V7boLBI7WSpEWHniGs/giphy.gif">

# И так, какие средства у нас используются

1. [gitleaks](https://github.com/zricethezav/gitleaks)
   Локальный запуск

```shell
docker run -v ${PWD}:/path zricethezav/gitleaks:latest detect --source="/path" -v
````

2. [Trivy](https://aquasecurity.github.io/trivy/v0.37/tutorials/overview/)
   Локальный запуск

```shell
docker run -v /var/run/docker.sock:/var/run/docker.sock -v ${PWD}:/path aquasec/trivy:0.37.1 fs /path
DOCKER_HOST="unix://var/run/docker.sock" docker run -v /var/run/docker.sock:/var/run/docker.sock -v /run/containerd/containerd.sock:/run/containerd/containerd.sock -v ${PWD}:/path aquasec/trivy:0.37.1 image registry.gitlab.idacloud.ru/idaproject/internal/template_project/nginx
```
3. [ZapProxy](https://www.zaproxy.org/)
   Локальный запуск

```shell
docker run -t owasp/zap2docker-stable zap-baseline.py -t https://glorax.com
```
