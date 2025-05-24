import sys
import json
from datetime import datetime

def greet(name="World"):
    """Return a greeting message"""
    return f"Hello {name} from Jenkins Pipeline!"

def get_system_info():
    """Get basic system information"""
    return {
        "python_version": sys.version,
        "timestamp": datetime.now().isoformat(),
        "platform": sys.platform
    }

def main():
    print("=" * 50)
    print(greet())
    print("=" * 50)
    
    print("\nSystem Information:")
    info = get_system_info()
    print(json.dumps(info, indent=2))
    
    print("\nBuild completed successfully!")
    print("=" * 50)
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
