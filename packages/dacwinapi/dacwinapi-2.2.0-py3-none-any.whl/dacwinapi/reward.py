try:
	from base import BaseService
	from utils.models import Reward
except:
	from .base import BaseService
	from .utils.models import Reward


class RewardService(BaseService):
	url = BaseService.url + "/api/v1/apps/rewards/"
	Entity = Reward
	EntityDetail = Reward
	
	def getAll(self, campaign_id: int=None) -> [Reward]: 
		if campaign_id:
			# Get a list of Rewards associated with a specific Campaign ID
			return super().getAll(campaign=campaign_id)
		else:
			# Get a list of all Rewards if no specific Campaign ID is provided
			return super().getAll()
		
	def getOne(self, id: int) -> Reward:
		"""
		Get details of a specific Reward by ID
		"""

		return super().getOne(id)
