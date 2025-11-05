import logging
import sys

def configure_logging():
    """Configura o logger principal da aplicação."""
    root = logging.getLogger()
    if root.handlers:
        return
    
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s %(levelname)s - %(name)s %(message)s")
    handler.setFormatter(formatter)
    
    root.setLevel(logging.INFO)
    root.addHandler(handler)
