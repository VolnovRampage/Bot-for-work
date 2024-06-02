import zipfile
import os
import aiofiles

from tqdm.asyncio import tqdm


path_to_archive: str = os.path.join(os.getcwd(), 'archive')
path_to_zip: str = os.path.join(path_to_archive, 'archive.zip')
path: str = '/Users/rampage/Desktop/test/'
start_path: str = '/Users/rampage/Desktop/'


async def create_archive() -> None:
    with zipfile.ZipFile(
        file= path_to_zip, mode='w',
        compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as zip:
        amount: int = sum(len(files) for _, _, files in os.walk(path))
        with tqdm(initial=amount, desc='Архивация', unit=' Файлов') as pbar:
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, start_path)
                    async with aiofiles.open(file_path, 'rb') as f:
                        content = await f.read()
                        zip.writestr(rel_path, content)
                    pbar.update(1)


async def extract_archive()  -> None:
    with zipfile.ZipFile(file=path_to_zip) as zip:
        zip.extractall(path=path_to_archive)
