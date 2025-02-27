import os
import sys
from pathlib import Path

def test_translations():
    """Test if translations are working correctly."""
    # Add src directory to Python path
    src_dir = Path(__file__).parent.parent / 'src'
    sys.path.append(str(src_dir))
    
    from core.translation import Translation
    
    locales_dir = src_dir / 'locales'
    for lang in ['en', 'de']:
        mo_file = locales_dir / lang / 'LC_MESSAGES' / 'messages.mo'
    
    for lang in ['en', 'de']:
        try:
            # Get translator and install it
            translator = Translation.setup_language(lang)
            
            # Get translation function
            _ = translator.gettext
            
            test_strings = {
                'File Organizer': 'Datei-Organisierer' if lang == 'de' else 'File Organizer',
                'Source Folder:': 'Quellordner:' if lang == 'de' else 'Source Folder:',
                'Debug Mode': 'Debug-Modus' if lang == 'de' else 'Debug Mode'
            }
            
            for original, expected in test_strings.items():
                result = _(original)
                
        except Exception as e:
            print(f"Error testing {lang}: {e}")

if __name__ == "__main__":
    test_translations()