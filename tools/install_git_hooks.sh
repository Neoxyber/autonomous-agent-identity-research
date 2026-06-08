#!/usr/bin/env sh
set -eu

repo_root="$(git rev-parse --show-toplevel)"
hook_path="$repo_root/.git/hooks/pre-commit"

cat > "$hook_path" <<'EOF'
#!/usr/bin/env sh
set -eu

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

python tools/secret_scan.py --staged
EOF

chmod +x "$hook_path"
printf 'Installed local pre-commit hook: %s\n' "$hook_path"
