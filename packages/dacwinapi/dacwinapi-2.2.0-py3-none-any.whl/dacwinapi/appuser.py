import requests

try:
	from base import BaseService
	from utils.models import AppUser, AppUserDetail
except:
	from .base import BaseService
	from .utils.models import AppUser, AppUserDetail


class AppUserService(BaseService):
	url = BaseService.url + "/api/v1/referrals/app-users/"
	Entity = AppUser
	EntityDetail = AppUserDetail

	def create(self, reference: str, referrer_referral_code: str=None) -> AppUser:
		"""
		Create a new app user and return the created app user as AppUser object
		""" 

		data = {
			"reference": reference
		}

		if referrer_referral_code is not None:
			data["referrer_referral_code"] = referrer_referral_code

		res = requests.post(
			url=self.url,
			json=data,
			headers=self.request_headers
		)

		if res.status_code == 201:
			app_user = AppUser(data=res.json())
		elif res.status_code == 401:
			raise ValueError(f"status code: {res.status_code}, The API key is invalid")
		else:
			raise ValueError(f"status code: {res.status_code}, response: {res.json()}")

		return app_user

	def getAll(self) -> [AppUser]: 
		"""
		Get a list of all AppUsers.

		Returns:
			[AppUser]: A list of AppUser objects.

		Raises:
			ValueError: If the API request fails.
		"""

		return super().getAll()

	def getOne(self, id: int=None, reference: str=None) -> AppUserDetail:
		"""
		Get details of a specific AppUser by ID or reference

		Returns:
			AppUserDetail: A AppUserDetail object.

		Raises:
			ValueError: If the API request fails.
		"""

		url = self.url

		if id is not None and reference is not None:
			raise ValueError("The two arguments id and reference cannot be defined together. Define just one of the two")
		elif id is not None:
			url += f"{id}/"
		elif reference is not None:
			url += f"{reference}/?reference=true"
		else:
			raise ValueError("Define at least one of the two arguments, id or reference")

		res = requests.get(
			url=url,
			headers=self.request_headers
		)

		if res.status_code == 200:
			app_user = AppUserDetail(data=res.json())
		elif res.status_code == 404:
			app_user = None
		elif res.status_code == 401:
			raise ValueError(f"status code: {res.status_code}, The API key is invalid")
		else:
			raise ValueError(f"status code: {res.status_code}, response: {res.json()}")
		
	
		return app_user
