"""Gunicorn config: settings and hooks are read by name, not imported."""

# Network — gunicorn does getattr(config, "bind") etc. at startup.
bind = "0.0.0.0:80"
forwarded_allow_ips = "*"
secure_scheme_headers = {"X-FORWARDED-PROTO": "https"}

# Worker processes
workers = 4
threads = 1
worker_class = "sync"
timeout = 15
graceful_timeout = 10

# Application
chdir = "/usr/src/app"
preload_app = True
control_socket_disable = True


def worker_exit(server, worker):  # noqa: ARG001
    """Called by gunicorn via config.worker_exit(server, worker)."""
    server.log.info("worker %s exiting", worker.pid)
