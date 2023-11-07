try:
	from base import BaseService
	from utils.models import RewardCondition, App
except:
	from .base import BaseService
	from .utils.models import RewardCondition, App

class Campaign:
	def __init__(self, data: dict):
		"""
		Initialize the Campaign object with data from a dictionary
		"""
		
		self.id: int = data["id"]
		self.app: int = data["app"]
		self.name: str = data["name"]
		self.description: str = data["description"]
		self.reward_type: str = data["reward_type"]
		self.reward_value: str = data["reward_value"]
		self.reward_the_referred_user: bool = data["reward_the_referred_user"]
		self.required_referred_users_count: int = data["required_referred_users_count"]
		self.user_rewards_limit: int | None = data.get("user_rewards_limit")
		self.active: bool = data["active"]
		self.start_date: str = data["start_date"]
		self.end_date: str | None = data.get("end_date")
		self.created_at: str = data["created_at"]
		self.updated_at: str = data["updated_at"]
	
	def __repr__(self):
		return f"Campaign(id={self.id}, name={self.name})"

class CampaignDetail(Campaign):
	def __init__(self, data: dict):
		super().__init__(data)

		# Additional attributes for CampaignDetail
		self.app: App = App(data=data["app"])
		self.reward_conditions: [RewardCondition] = [RewardCondition(data=i) for i in data["reward_conditions"]]




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

# Define a main function for testing
def main():
	api_key = ""

	# campaignService = CampaignService(api_key=api_key)

	# print(campaignService.getAll())
	# print(campaignService.getOne(id=18))
	

if __name__ == "__main__":
	main()