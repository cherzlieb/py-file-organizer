import os
import sys
from pathlib import Path
import re

def find_translation_strings():
    """Find all strings marked for translation in the code."""
    src_dir = Path(__file__).parent.parent / 'src'

    translation_strings = set()
    pattern = re.compile(r'_\(["\']([^"\']+)["\'][\),]')

    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    matches = pattern.findall(content)
                    translation_strings.update(matches)

    return translation_strings

def check_po_file(po_path, translation_strings):
    """Check if all translation strings are in the PO file."""
    if not os.path.exists(po_path):
        print(f"Error: PO file not found at {po_path}")
        return

    with open(po_path, 'r', encoding='utf-8') as f:
        content = f.read()

    missing = []
    for string in translation_strings:
        pattern = f'msgid "{string}"'
        if pattern not in content:
            missing.append(string)

    return missing

def main():
    """Check for missing translations."""
    src_dir = Path(__file__).parent.parent / 'src'
    translation_strings = find_translation_strings()

    print(f"Found {len(translation_strings)} strings marked for translation")

    for lang in ['en', 'de']:
        po_path = src_dir / 'locales' / lang / 'LC_MESSAGES' / 'messages.po'
        missing = check_po_file(po_path, translation_strings)

        if missing:
            print(f"\nMissing translations in {lang}:")
            for string in missing:
                print(f'msgid "{string}"\nmsgstr ""\n')
        else:
            print(f"\nNo missing translations in {lang}")

if __name__ == "__main__":
    main()
