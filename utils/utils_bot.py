import os.path
from aiogram.types import input_file, FSInputFile
from aiogram import types


async def get_photo(name: str) -> FSInputFile:
    return types.FSInputFile(name)


async def get_prompt(name: str) -> str:
    result = None
    try:
        with open(os.path.join('resources', 'prompts', name+'.txt'), 'r', encoding='UTF-8') as f:
            result = f.read()
    except FileNotFoundError:
        result = 'not found'
    return result