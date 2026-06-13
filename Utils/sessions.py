from aiohttp import ClientSession, web_exceptions
from pydantic import BaseModel
import asyncio


session: ClientSession | None = None
_session_lock = asyncio.Lock()

async def get_session() -> ClientSession:
	'''
	Create a session if none exists, returns existing otherwise
	'''
	global session
	async with _session_lock:
		if session is None or session.closed:
			session = ClientSession()
		
		return session

async def close_session() -> None:
	global session

	if session and not session.closed:
		await session.close()
		session = None

async def fetch_data[T: BaseModel](url: str, model: type[T]) -> T:
	'''														
	Fetches response from an API that's passed in
	then validates it against a defined model and returned
	'''
	sesh = await get_session()
	async with sesh.get(url=url) as response:
		model = model.model_validate(await response.json())

	return model
