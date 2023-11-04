import requests

try:
	from base import BaseService
	from campaign import CampaignDetail
	from appuser import AppUser
except:
	from .base import BaseService
	from .campaign import CampaignDetail
	from .appuser import AppUser




class Event:
	def __init__(self, data: dict):
		self.id: int = data["id"]
		self.campaign: int = data["campaign"]
		self.app_user: int = data["app_user"]
		self.name: str = data["name"]
		self.created_at: str = data["created_at"]
		self.updated_at: str = data["updated_at"]

	def __repr__(self):
		return f"Event(id={self.id}, name={self.name}, app_user={self.app_user.id})"

class EventDetail(Event):
	def __init__(self, data: dict):
		super().__init__(data)

		self.campaign: CampaignDetail = CampaignDetail(data=data["campaign"])
		self.app_user: AppUser = AppUser(data=data["app_user"])


class EventService(BaseService):
	url = BaseService.url + "/api/v1/apps/events/"
	Entity = Event
	EntityDetail = EventDetail

	def create(self, name: str, campaign_id: int, app_user_id: int) -> Event:
		data = {
			"campaign": campaign_id,
			"app_user": app_user_id,
			"name": name
		}

		res = requests.post(
			url=self.url,
			json=data,
			headers=self.request_headers
		)

		if res.status_code == 201:
			event = Event(data=res.json())
		elif res.status_code == 401:
			raise ValueError(f"status code: {res.status_code}, The API key is invalid")
		else:
			raise ValueError(f"status code: {res.status_code}, response: {res.json()}")

		return event

	def getAll(self) -> [Event]: 
		return super().getAll()
	
	def getOne(self, id: int) -> [EventDetail]: 
		return super().getOne(id)


def main():
	api_key = "O8GAbM8D.czZH7plW7mE6SjBmADzHbKXvJNUehcVi"

	eventService = EventService(api_key=api_key)

	print(eventService.getAll())
	print(eventService.getOne(id=1))

	event_created = eventService.create(
		name="ddd",
		campaign_id=18,
		app_user_id=14
	)

	print(event_created)
	

if __name__ == "__main__":
	main()