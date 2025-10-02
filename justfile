up:
    podman kube play local-dev.yaml

down:
    podman kube down local-dev.yaml

build:
    podman build -t redics .

check: lint type-check

lint:
    ruff check

alias tc := type-check
type-check:
    pyrefly check
