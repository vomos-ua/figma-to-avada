"""
Generate shortcode catalog from Avada Fusion Builder PHP source.

Parses get_element_defaults() and add_shortcode() in each PHP file under
fusion-builder/shortcodes/ and fusion-core/shortcodes/.

Output: catalog.json + catalog.md (human-readable summary).

Run:
    python _catalog-generator.py
"""

import os
import re
import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

PLUGINS = [
    Path(r"D:\AI\Linked Promo\docs\Avada\fusion-builder\shortcodes"),
    Path(r"D:\AI\Linked Promo\docs\Avada\fusion-builder\inc"),
    Path(r"D:\AI\Linked Promo\docs\Avada\fusion-core\shortcodes"),
]
OUT_DIR = Path(__file__).parent

# Capture shortcode names from add_shortcode() OR constructor-style '$shortcode = "..."'
SHORTCODE_NAME_RE = re.compile(
    r"(?:add_shortcode\(\s*['\"]([a-z_][a-z0-9_]*)['\"]|\$shortcode\s*=\s*['\"]([a-z_][a-z0-9_]*)['\"])",
    re.IGNORECASE,
)
DEFAULTS_FN_RE = re.compile(
    r"function\s+get_element_defaults\s*\([^)]*\)\s*\{(.*?)return\s+(\[[^;]*?\]\s*;)",
    re.DOTALL,
)

# Match key => value pairs at the top level of a PHP array literal.
# value can be a quoted string, numeric, true/false/null, a call expression
# (we capture whatever is on the right up to the next `,` or end).
PAIR_RE = re.compile(
    r"['\"]([a-zA-Z_][a-zA-Z0-9_]*)['\"]\s*=>\s*([^,\n]+?)(?=\s*,\s*\n|\s*,?\s*\]|\s*,\s*//|$)",
    re.MULTILINE,
)


def parse_value(raw: str) -> object:
    """Best-effort parse of a PHP scalar/expression default into a JSON-friendly form."""
    s = raw.strip().rstrip(",").strip()
    if not s:
        return ""
    # Quoted string
    m = re.match(r"^'([^']*)'$", s)
    if m:
        return m.group(1)
    m = re.match(r'^"([^"]*)"$', s)
    if m:
        return m.group(1)
    # Boolean / null
    low = s.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if low == "null":
        return None
    # Integer
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    # Float
    if re.fullmatch(r"-?\d+\.\d+", s):
        return float(s)
    # Function/method call (fusion_settings->get('foo'), fusion_builder_default_visibility(...)).
    # Mark as dynamic.
    if "(" in s and ")" in s:
        return {"_dynamic": s}
    # Fallback: return raw string with marker
    return {"_unparsed": s}


def extract_defaults_array(php_text: str) -> dict | None:
    m = DEFAULTS_FN_RE.search(php_text)
    if not m:
        return None
    body = m.group(2)
    pairs = {}
    for key, val in PAIR_RE.findall(body):
        pairs[key] = parse_value(val)
    return pairs


def extract_shortcode_name(php_text: str) -> str | None:
    m = SHORTCODE_NAME_RE.search(php_text)
    if not m:
        return None
    # Group 1 = from add_shortcode(), group 2 = from $shortcode = '...'
    return m.group(1) or m.group(2)


def crawl_plugin(plugin_dir: Path) -> list[dict]:
    entries = []
    for php_path in sorted(plugin_dir.rglob("*.php")):
        rel = php_path.relative_to(plugin_dir)
        try:
            text = php_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = php_path.read_text(encoding="latin-1")
        sc_name = extract_shortcode_name(text)
        defaults = extract_defaults_array(text)
        if not sc_name and not defaults:
            continue
        entries.append({
            "file": str(rel).replace("\\", "/"),
            "plugin": plugin_dir.parent.name,
            "shortcode": sc_name,
            "param_count": len(defaults) if defaults else 0,
            "defaults": defaults or {},
        })
    return entries


def main():
    all_entries = []
    for plugin in PLUGINS:
        if not plugin.exists():
            print(f"WARN: plugin path not found: {plugin}")
            continue
        entries = crawl_plugin(plugin)
        all_entries.extend(entries)
        print(f"  {plugin.parent.name}/{plugin.name}: {len(entries)} shortcodes")

    # Write full catalog JSON
    catalog_path = OUT_DIR / "catalog.json"
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(all_entries, f, ensure_ascii=False, indent=2)
    print(f"\nWrote {catalog_path} ({catalog_path.stat().st_size} bytes)")

    # Write human-readable summary
    md_path = OUT_DIR / "catalog.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Avada shortcode catalog\n\n")
        f.write(f"Generated from {len(all_entries)} PHP files.\n\n")

        with_name = [e for e in all_entries if e["shortcode"]]
        without_name = [e for e in all_entries if not e["shortcode"]]
        f.write(f"- {len(with_name)} shortcodes have a registered name\n")
        f.write(f"- {len(without_name)} files have defaults but no `add_shortcode()` (likely inner components)\n\n")

        # Group by plugin
        by_plugin: dict[str, list[dict]] = {}
        for e in all_entries:
            by_plugin.setdefault(e["plugin"], []).append(e)

        for plugin, entries in by_plugin.items():
            f.write(f"## {plugin}\n\n")
            f.write("| Shortcode | File | Params |\n|---|---|---|\n")
            for e in sorted(entries, key=lambda x: (x["shortcode"] or "", x["file"])):
                name = f"`[{e['shortcode']}]`" if e["shortcode"] else "*(no name)*"
                f.write(f"| {name} | `{e['file']}` | {e['param_count']} |\n")
            f.write("\n")

    print(f"Wrote {md_path}")
    print(f"\nTotal: {len(all_entries)} shortcode definitions")


if __name__ == "__main__":
    main()
