#!/usr/bin/env python3
import os
import sys


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_ROOT = os.path.join(REPO_ROOT, "src")
APPS = ("tests",)


def _db_settings():
    db_engine = os.environ.get("DJANGO_DB_ENGINE", "sqlite")
    if db_engine == "mysql":
        return {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.environ["DJANGO_DB_NAME"],
            "USER": os.environ["DJANGO_DB_USER"],
        }
    if db_engine == "postgres":
        return {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ["DJANGO_DB_NAME"],
            "USER": os.environ["DJANGO_DB_USER"],
        }
    if db_engine == "sqlite":
        return {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(REPO_ROOT, "database.db"),
        }

    raise ValueError(f"Unknown DB engine: {db_engine}")


def main():
    if REPO_ROOT not in sys.path:
        sys.path.insert(0, REPO_ROOT)
    if SRC_ROOT not in sys.path:
        sys.path.insert(0, SRC_ROOT)

    from django.conf import settings

    if not settings.configured:
        settings.configure(
            DEBUG=True,
            DATABASES={"default": _db_settings()},
            CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}},
            INSTALLED_APPS=APPS,
        )

    import django
    import pytest

    django.setup()
    return pytest.main(["tests/"])


if __name__ == "__main__":
    sys.exit(main())
