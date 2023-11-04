from base import BaseService
from appuser import AppUser
from campaign import Campaign, CampaignDetail

class Reward:
	def __init__(self, data: dict):
		self.id: int = data["id"]
		self.campaign: CampaignDetail = CampaignDetail(data=data["campaign"])
		self.app_user: AppUser = AppUser(data=data["app_user"])
		self.app_user_type: str = data["app_user_type"]
		self.created_at: str = data["created_at"]
		self.updated_at: str = data["updated_at"]
	
	def __repr__(self):
		return f"Reward(id={self.id}, app_user_id={self.app_user.id})"


class RewardService(BaseService):
	url = BaseService.url + "/api/v1/apps/rewards/"
	Entity = Reward
	EntityDetail = Reward
	
	def getAll(self, campaign_id: int=None) -> [Reward]: 

		if campaign_id:
			return super().getAll(campaign=campaign_id)
		else:
			return super().getAll()
		
	def getOne(self, id: int) -> Reward:
		return super().getOne(id)

def main():
	api_key = "O8GAbM8D.czZH7plW7mE6SjBmADzHbKXvJNUehcVi"

	rewardService = RewardService(api_key=api_key)

	print(rewardService.getAll(campaign_id=18))
	# print(rewardService.getOne(id=12))
	

if __name__ == "__main__":
	main()