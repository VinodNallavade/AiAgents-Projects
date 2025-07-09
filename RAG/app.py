from src.ui.main import load_app
import asyncio
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


if __name__ == "__main__":
    asyncio.run(load_app())