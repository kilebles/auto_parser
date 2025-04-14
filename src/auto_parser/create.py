import asyncio
from auto_parser.generate_matrix import generate_matrix

if __name__ == "__main__":
    asyncio.run(generate_matrix(days=30))
