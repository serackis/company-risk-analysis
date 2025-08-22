#!/usr/bin/env python3
"""
Startup script for Company Risk Analysis System
"""

import os
import sys
from app import app

if __name__ == '__main__':
    # Set environment variables
    os.environ['FLASK_ENV'] = 'development'
    
    # Get port from command line or use default
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    
    print("🚀 Starting Company Risk Analysis System...")
    print(f"📱 Application will be available at: http://localhost:{port}")
    print("🔄 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        app.run(
            host='0.0.0.0',
            port=port,
            debug=True,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)
