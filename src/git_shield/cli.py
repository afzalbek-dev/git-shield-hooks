"""CLI for Git Shield."""
import sys
import argparse
from .scanner import ShieldScanner
from .installer import install_pre_commit_hook

def main():
    parser = argparse.ArgumentParser(description="Git Shield — Pre-commit Security & Secrets Leak Scanner")
    subparsers = parser.add_subparsers(dest="command", help="Mavjud buyruqlar")

    # scan
    scan_p = subparsers.add_parser("scan", help="Katalog yoki fayllarni maxfiy kalitlar uchun skanlash")
    scan_p.add_argument("--path", default=".", help="Skaner qilinadigan katalog yo'li")
    scan_p.add_argument("--max-size", type=float, default=10.0, help="Maksimal fayl hajmi (MB)")

    # install-hook
    inst_p = subparsers.add_parser("install-hook", help="Joriy repozitoriyga avtomatik pre-commit hook o'rnatish")
    inst_p.add_argument("--repo", default=".", help="Git repozitoriya katalogi")

    args = parser.parse_args()
    scanner = ShieldScanner(max_file_size_mb=args.max_size if hasattr(args, "max_size") else 10.0)

    if args.command == "scan" or not args.command:
        target_path = getattr(args, "path", ".")
        findings = scanner.scan_directory(target_path)
        print("\n🛡️  GIT SHIELD — XAVFSIZLIK AUDITI")
        print("────────────────────────────────────────────────────────────")
        if not findings:
            print(f"✅ Skanlash toza! '{target_path}' ichida hech qanday maxfiy sirlar topilmadi.\n")
            sys.exit(0)
        else:
            print(f"🚨 DIQQAT! {len(findings)} ta potensial maxfiylik yoki muammo aniqlandi:\n")
            for f in findings:
                print(f"  ❌ [{f['type']}] Fayl: {f['file']}:{f['line']}")
                print(f"     ↳ {f['snippet']}")
            print("\n❌ Git Shield: Iltimos, ushbu sirlarni .gitignore yoki .env ga o'tkazing!\n")
            sys.exit(1)

    elif args.command == "install-hook":
        repo_dir = getattr(args, "repo", ".")
        ok = install_pre_commit_hook(repo_dir)
        if ok:
            print(f"✅ Git Shield pre-commit hook '{repo_dir}/.git/hooks/pre-commit' ga muvaffaqiyatli o'rnatildi!")
        else:
            print(f"❌ Xatolik: '{repo_dir}' papkasida .git katalogi topilmadi!")
            sys.exit(1)

if __name__ == "__main__":
    main()
