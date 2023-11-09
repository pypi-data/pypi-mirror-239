try:
	from base import BaseService
	from utils.models import Campaign, CampaignDetail
except:
	from .base import BaseService
	from .utils.models import Campaign, CampaignDetail


class CampaignService(BaseService):
	url = BaseService.url + "/api/v1/apps/campaigns/"
	Entity = Campaign
	EntityDetail = CampaignDetail
	
	def getAll(self) -> [Campaign]:
		"""
		Get a list of all Campaigns of the app
		"""															
		
		return super().getAll()
		
	def getOne(self, id: int) -> CampaignDetail:
		"""
		Get details of a specific Campaign by ID
		"""

		return super().getOne(id)
