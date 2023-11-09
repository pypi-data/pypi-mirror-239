import requests

try:
	from base import BaseService
	from utils.models import Event, EventDetail
except:
	from .base import BaseService
	from .utils.models import Event, EventDetail


class EventService(BaseService):
	url = BaseService.url + "/api/v1/apps/events/"
	Entity = Event
	EntityDetail = EventDetail

	def create(self, name: str, campaign_id: int, app_user_id: int) -> Event:
		"""
		Create event for specific app user and campaign
		"""

		# body of the creation request
		data = {
			"campaign": campaign_id,
			"app_user": app_user_id,
			"name": name
		}
		
		# create event
		res = requests.post(
			url=self.url,
			json=data,
			headers=self.request_headers
		)
		
		# retrieve event data object or raise exception
		if res.status_code == 201:
			event = Event(data=res.json())
		elif res.status_code == 401:
			raise ValueError(f"status code: {res.status_code}, The API key is invalid")
		else:
			raise ValueError(f"status code: {res.status_code}, response: {res.json()}")

		return event

	def getAll(self, campaign_id: int=None) -> [Event]: 
		"""
		Get a list of events
		"""

		if campaign_id:
			# Get a list of events associated with a specific Campaign ID
			return super().getAll(campaign=campaign_id)
		else:
			# Get a list of all events if no specific Campaign ID is provided
			return super().getAll()

	def getOne(self, id: int) -> [EventDetail]: 
		"""
		Get details of a specific event by ID
		"""

		return super().getOne(id)
