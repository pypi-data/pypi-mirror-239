import requests

try:
	from base import BaseService
except:
	from .base import BaseService

class AppUser:
	def __init__(self, data: dict):
		"""
		Initialize the AppUser object with data from a dictionary
		"""

		self.id: int = data["id"]
		self.app: int = data["app"]
		self.reference: str = data["reference"]
		self.referral_code: str = data["referral_code"]
		self.referrer: int | None = data.get("referrer")
		self.created_at: str = data["created_at"]
		self.updated_at: str = data["updated_at"]
		self.is_active: bool = data["is_active"]
	
	def __repr__(self):
		return f"AppUser(id={self.id}, ref={self.reference})"

class AppUserDetail(AppUser):
	def __init__(self, data: dict):
		"""
		Initialize an AppUserDetail object with additional data.

		Args:
			data (dict): A dictionary containing AppUserDetail data.
		"""

		super().__init__(data)
		
		# import Reward class
		try:
			from reward import Reward
		except:
			from .reward import Reward

		# Additional attributes for AppUserDetail
		self.app: int = data["app"]  # : App
		self.referrer: AppUser | None = data.get("referrer")
		self.referred_users: [AppUser] = data["referred_users"]
		self.rewards: [Reward] = data["rewards"]


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

# Define a main function for testing
def main():
	api_key = "O8GAbM8D.czZH7plW7mE6SjBmADzHbKXvJNUehcVi"

	appUserService = AppUserService(api_key=api_key)

	print(appUserService.getAll())
	print(appUserService.getOne(reference="1Pxdd6tZiPWPam3QEpGIkywo51H3"))

	# app_user_created = appUserService.create(
	# 	reference="3"
	# )

	# print(app_user_created)
	

if __name__ == "__main__":
	main()