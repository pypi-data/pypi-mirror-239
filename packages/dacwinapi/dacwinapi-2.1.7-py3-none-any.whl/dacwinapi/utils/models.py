
class App:
	def __init__(self, data: dict):
		self.id: int = data["id"]
		self.name: str = data["name"]
		self.reward_callback_url: str = data.get("reward_callback_url")
		self.user: int = data["user"]
		self.created_at: str = data["created_at"]
		self.updated_at: str = data["updated_at"]

class RewardCondition:
	def __init__(self, data: dict):
		self.id: int = data["id"]
		self.campaign: int = data["campaign"]
		self.event_name: str = data["event_name"]
		self.event_count_per_referred_user: int = data["event_count_per_referred_user"]
		self.created_at: str = data["created_at"]
		self.updated_at: str = data["updated_at"]
