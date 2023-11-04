from base import BaseService

class Campaign:
	def __init__(self, data: dict):
		self.id: int = data["id"]
		self.app: int = data["app"]
		self.name: str = data["name"]
		self.description: str = data["description"]
		self.reward_type: str = data["reward_type"]
		self.reward_value: str = data["reward_value"]
		self.reward_the_referred_user: bool = data["reward_the_referred_user"]
		self.required_referred_users_count: int = data["required_referred_users_count"]
		self.user_rewards_limit: int | None = data["user_rewards_limit"]
		self.active: bool = data["active"]
		self.start_date: str = data["start_date"]
		self.end_date: str | None = data["end_date"]
		self.created_at: str = data["created_at"]
		self.updated_at: str = data["updated_at"]
	
	def __repr__(self):
		return f"Campaign(id={self.id}, name={self.name})"

class CampaignDetail(Campaign):
	def __init__(self, data: dict):
		super().__init__(data)

		self.app: int = data["app"] # : App
		self.reward_conditions: [str] = data["reward_conditions"] # : [RewardCondition]

# "app": {
#         "id": 1,
#         "name": "APP",
#         "reward_callback_url": null,
#         "user": 2,
#         "created_at": "2023-08-28T09:55:10.555394Z",
#         "updated_at": "2023-08-28T09:55:10.555436Z"
#     },
#     "reward_conditions": [
#         {
#             "id": 3,
#             "campaign": 1,
#             "event_name": "INSCRIPTION",
#             "event_count_per_referred_user": 1,
#             "created_at": "2023-08-29T17:12:01.029134Z",
#             "updated_at": "2023-08-29T17:12:01.029162Z"
#         }
#     ],

class CampaignService(BaseService):
	url = BaseService.url + "/api/v1/apps/campaigns/"
	Entity = Campaign
	EntityDetail = CampaignDetail
	
	def getAll(self) -> [Campaign]: 															
		return super().getAll()
		
	def getOne(self, id: int) -> CampaignDetail:
		return super().getOne(id)

def main():
	api_key = "O8GAbM8D.czZH7plW7mE6SjBmADzHbKXvJNUehcVi"

	campaignService = CampaignService(api_key=api_key)

	print(campaignService.getAll())
	print(campaignService.getOne(id=18))
	

if __name__ == "__main__":
	main()