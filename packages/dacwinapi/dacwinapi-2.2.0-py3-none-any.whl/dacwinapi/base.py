import requests

try:
	from utils.constants import DACWIN_API_BASE_URL
except:
	from .utils.constants import DACWIN_API_BASE_URL

class BaseService:
	url = DACWIN_API_BASE_URL
	Entity = None
	EntityDetail = None

	def __init__(self, api_key: str):
		self.api_key = api_key

		self.request_headers = {
			"Api-Key": self.api_key
		}
	
	def getAll(self, **params):
		params_string = "&".join([f"{key}={value}" for key, value in params.items()])

		res = requests.get(
			url=self.url + f"?{params_string}",
			headers=self.request_headers
		)

		if res.status_code == 200:
			entities = [self.Entity(data=data) for data in res.json()]
		elif res.status_code == 401:
			raise ValueError(f"status code: {res.status_code}, The API key is invalid")
		else:
			raise ValueError(f"status code: {res.status_code}, response: {res.json()}")

		return entities

	def getOne(self, id: int):
		res = requests.get(
			url=self.url + f"{id}/",
			headers=self.request_headers
		)

		if res.status_code == 200:
			entity = self.EntityDetail(data=res.json())
		elif res.status_code == 404:
			entity = None
		elif res.status_code == 401:
			raise ValueError(f"status code: {res.status_code}, The API key is invalid")
		else:
			raise ValueError(f"status code: {res.status_code}, response: {res.json()}")
		
	
		return entity