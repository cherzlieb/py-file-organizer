from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po
import os

def compile_translations():
    """Compile .po files to .mo files using babel."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    locales_dir = os.path.join(base_dir, 'src', 'locales')
    
    for lang in ['de', 'en']:
        po_file = os.path.join(locales_dir, lang, 'LC_MESSAGES', 'messages.po')
        mo_file = os.path.join(locales_dir, lang, 'LC_MESSAGES', 'messages.mo')
        
        # Create LC_MESSAGES directory if it doesn't exist
        os.makedirs(os.path.dirname(mo_file), exist_ok=True)
        
        try:
            # Remove existing .mo file if it exists
            if os.path.exists(mo_file):
                os.remove(mo_file)
                
            with open(po_file, 'rb') as po_input:
                catalog = read_po(po_input)
            
            with open(mo_file, 'wb') as mo_output:
                write_mo(mo_output, catalog)
                
            print(f"Successfully compiled {po_file} to {mo_file}")
        except Exception as e:
            print(f"Error compiling {po_file}: {e}")

if __name__ == "__main__":
    compile_translations()