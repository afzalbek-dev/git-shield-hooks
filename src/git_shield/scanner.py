"""Git security scanner for secrets, tokens, and oversized binaries."""
import re
import os
import math
from typing import List, Dict, Any, Optional

SECRET_PATTERNS = [
    ("GitHub Personal Access Token", re.compile(r"gh[pousr]_[A-Za-z0-9_]{30,255}")),
    ("Telegram Bot Token", re.compile(r"\b\d{8,11}:[A-Za-z0-9_-]{35}\b")),
    ("AWS Access Key ID", re.compile(r"\b(AKIA|ABIA|ACCA|ASIA)[0-9A-Z]{16}\b")),
    ("Private Key Header", re.compile(r"-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----")),
    ("Generic API Key Assignment", re.compile(r"""(?i)(api[_-]?key|secret[_-]?key|auth[_-]?token)\s*[:=]\s*['"][A-Za-z0-9_\-\.]{16,}['"]""")),
    ("JWT Token", re.compile(r"\beyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"))
]

IGNORED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".lock", ".pyc", ".db", ".sqlite"}

class ShieldScanner:
    def __init__(self, max_file_size_mb: float = 10.0):
        self.max_file_size_bytes = int(max_file_size_mb * 1024 * 1024)

    def calculate_shannon_entropy(self, text: str) -> float:
        """Calculates Shannon entropy of a string to detect high-entropy keys."""
        if not text:
            return 0.0
        prob = [float(text.count(c)) / len(text) for c in set(text)]
        return -sum([p * math.log2(p) for p in prob])

    def scan_content(self, text: str, file_path: str = "") -> List[Dict[str, Any]]:
        findings = []
        lines = text.splitlines()
        for idx, line in enumerate(lines, 1):
            for name, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    findings.append({
                        "file": file_path,
                        "line": idx,
                        "type": name,
                        "snippet": line[:60] + "..." if len(line) > 60 else line
                    })
        return findings

    def scan_file(self, file_path: str) -> List[Dict[str, Any]]:
        findings = []
        if not os.path.exists(file_path):
            return findings

        # Check file size
        size = os.path.getsize(file_path)
        if size > self.max_file_size_bytes:
            findings.append({
                "file": file_path,
                "line": 0,
                "type": "Oversized File",
                "snippet": f"Fayl hajmi {round(size / (1024**2), 2)}MB (Chegara: {self.max_file_size_bytes // (1024**2)}MB)"
            })

        ext = os.path.splitext(file_path)[1].lower()
        if ext in IGNORED_EXTENSIONS:
            return findings

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            findings.extend(self.scan_content(content, file_path=file_path))
        except Exception:
            pass

        return findings

    def scan_directory(self, target_dir: str = ".") -> List[Dict[str, Any]]:
        all_findings = []
        for root, dirs, files in os.walk(target_dir):
            if ".git" in dirs:
                dirs.remove(".git")
            if "node_modules" in dirs:
                dirs.remove("node_modules")
            if "__pycache__" in dirs:
                dirs.remove("__pycache__")

            for f in files:
                fp = os.path.join(root, f)
                all_findings.extend(self.scan_file(fp))
        return all_findings
