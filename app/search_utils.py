# app/search_utils.py

def is_valid_file(filename: str, allowed_exts) -> bool:
    return any(filename.lower().endswith(ext) for ext in allowed_exts)