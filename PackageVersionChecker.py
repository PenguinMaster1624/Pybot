import requests
import asyncio

async def api_call(package_name: str) -> str:
    with requests.get(url = f'https://pypi.org/pypi/{package_name}/json') as response:
        js = response.json()

    try:
        return js['info']['version']
    
    except KeyError as error:
        print(f'{error} is not a valid key')
    

async def package_check() -> None:
    '''
    Checks the versions within requirements.txt against the most up-to-date version on PyPI
    '''
    outdated = []
    with open('requirements.txt', mode = 'r', encoding = 'utf-8') as packages:
      for package in packages.readlines():
          info = package.replace('\n', '').split('==')
          latest_version = await api_call(info[0])

          if info[1] != latest_version:
              outdated.append(info[0])
    
    if outdated:
        print(f'These packages need to be updated: {outdated}')
        
    else:
        print('All packages up to date')

if __name__ == '__main__':
    asyncio.run(package_check())