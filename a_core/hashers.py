from __future__ import annotations

import os

from django.contrib.auth.hashers import PBKDF2PasswordHasher


class ConfigurablePBKDF2PasswordHasher(PBKDF2PasswordHasher):
    """PBKDF2 hasher with configurable iterations.

    Important: we never *downgrade* existing hashes (if an existing password was
    hashed with more iterations than the current config, it will be kept).

    Configure via env var:
    - PBKDF2_ITERATIONS
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        raw = (os.getenv("PBKDF2_ITERATIONS", "") or "").strip()
        if not raw:
            # Dev default: keep login/signup responsive on low-CPU machines.
            # Production default: keep Django's stock iterations unless explicitly overridden.
            if (os.getenv("ENVIRONMENT", "development") or "development").strip().lower() != "production":
                raw = "150000"

        if raw:
            try:
                iters = int(raw)
                if iters >= 100_000:
                    self.iterations = iters
            except Exception:
                pass

    def must_update(self, encoded: str) -> bool:
        # Default behavior would also rehash when stored iterations > current,
        # which would downgrade password strength. Avoid that.
        try:
            algorithm, iterations, _salt, _hash = encoded.split("$", 3)
            if algorithm != self.algorithm:
                return False
            stored_iters = int(iterations)
        except Exception:
            return False

        # Only update (rehash) when the stored hash is weaker.
        return stored_iters < int(getattr(self, "iterations", stored_iters))
