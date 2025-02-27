import gettext
import os
from typing import Dict, Optional

class Translation:
    LANGUAGES = {
        'en': 'English',
        'de': 'Deutsch'
    }
    
    _current_translator: Optional[gettext.NullTranslations] = None
    
    @staticmethod
    def setup_language(language: str) -> gettext.NullTranslations:
        """Setup language for the application."""
        try:
            # Get absolute path to locales directory
            locale_dir = os.path.abspath(os.path.join(
                os.path.dirname(__file__), 
                '..', 
                'locales'
            ))
            print(f"Loading translations from: {locale_dir}")
            print(f"Requested language: {language}")
            
            # Check if .mo file exists
            mo_path = os.path.join(locale_dir, language, 'LC_MESSAGES', 'messages.mo')
            if not os.path.exists(mo_path):
                print(f"Warning: Translation file not found at {mo_path}")
            else:
                print(f"Found translation file at {mo_path}")
            
            # Create translator
            translator = gettext.translation(
                'messages',
                localedir=locale_dir,
                languages=[language],
                fallback=True
            )
            
            # Test translation
            test_text = translator.gettext("File Organizer")
            print(f"Translation test: 'File Organizer' -> '{test_text}'")
            
            # Install globally
            translator.install()
            Translation._current_translator = translator
            
            return translator
            
        except Exception as e:
            print(f"Error setting up translation: {str(e)}")
            return gettext.NullTranslations()

    @staticmethod
    def get_language_names() -> Dict[str, str]:
        """Get available languages."""
        return Translation.LANGUAGES

    @staticmethod
    def get_translator() -> gettext.NullTranslations:
        """Get current translator."""
        if Translation._current_translator is None:
            return gettext.NullTranslations()
        return Translation._current_translator