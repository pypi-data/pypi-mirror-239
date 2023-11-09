
class App:
	def __init__(self, data: dict):
		self.id: int = data["id"]
		self.name: str = data["name"]
		self.reward_callback_url: str | None = data.get("reward_callback_url")
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


# ...

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


# ...


class Reward:
	def __init__(self, data: dict):
		"""
		Initialize the Reward object with data from a dictionary
		"""

		self.id: int = data["id"]
		self.campaign: CampaignDetail = CampaignDetail(data=data["campaign"])
		self.app_user: AppUser = AppUser(data=data["app_user"])
		self.app_user_type: str = data["app_user_type"]
		self.created_at: str = data["created_at"]
		self.updated_at: str = data["updated_at"]
	
	def __repr__(self):
		return f"Reward(id={self.id}, app_user_id={self.app_user.id})"

# ...


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

		# Additional attributes for AppUserDetail
		self.app: int = data["app"]  # : App
		self.referrer: AppUser | None = data.get("referrer")
		self.referred_users: [AppUser] = data["referred_users"]
		self.rewards: [Reward] = data["rewards"]

# ...


class Event:
	def __init__(self, data: dict):
		"""
		Initialize the Event object with data from a dictionary
		"""

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
