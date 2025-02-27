from pathlib import Path

def validate_paths(source: str, organized: str, unorganized: str) -> None:
    """Validate all input paths."""
    if not all([source, organized, unorganized]):
        raise ValueError("All paths must be specified")
    
    if not Path(source).exists():
        raise FileNotFoundError(f"Source path does not exist: {source}")