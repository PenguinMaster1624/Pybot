from utils.errors import OutdatedPackagesError
from utils.sessions import fetch_data
from models import VersionResponse
import asyncio


async def get_version() -> list[VersionResponse]:
    versions = []

    with open('requirements.txt') as file:
        for line in file.readlines():
            line = line.strip()
            if '==' in line:
                name, version = line.split('==')
            else:
                name = line
                version = None
            
            model = await fetch_data(url=f'https://pypi.org/pypi/{name}/json', model = VersionResponse)
            model.current = version
            versions.append(model)

    return versions

async def package_check() -> None:
    '''
    Checks the versions within requirements.txt against the most up-to-date version on PyPI
    '''
    
    packages = await get_version()
    outdated = [package.name for package in packages if package.current != package.latest and package.current is not None]

    if outdated:
        try:
            raise OutdatedPackagesError(outdated)
        
        except OutdatedPackagesError as error:
            print(error)


if __name__ == '__main__':
    asyncio.run(package_check())
