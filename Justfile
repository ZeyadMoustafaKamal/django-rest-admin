test:
  @uvx --with-requirements requirements/requirements-dev.txt pytest -s

lock:
  @uv pip compile requirements/requirements.in -o requirements.txt && uv pip compile requirements/requirements-dev.in -o requirements/requirements-dev.txt

