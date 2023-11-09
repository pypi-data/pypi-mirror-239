# DacWin API

The Python package dacwinapi makes it easy to manage information about your DacWin referral system. This package is specifically designed to interact with the DacWin API and allows you to manage information about an application's users, referral campaigns, rewards and events.

DacWin home page: https://referral-dev.dactechnologies.net

## Installation

To install `dacwinapi`, you can use pip:

```bash
pip install dacwinapi
```

Before using this package you must have the API key of the application you want to manage. If this is not the case yet,
- Go to your customer area: https://referral-devuser.dactechnologies.net
- In the `Applications` section:
	- Add an application and copy the generated API key.
	- Or, open your application's edit window and **regenerate a new API key** if you no longer have the old one.

## How to use this package

### 1. Campaigns

```python
from dacwinapi import CampaignService

# create an instance of CampaignService
campaignService = CampaignService(api_key="your_app_api_key")

# retrieve the list of campaigns of the app
campaigns = campaignService.getAll()

# retrieve one campaign data
campaigns = campaignService.getOne(1) # 1 is the campaign id 
```

> NOTE: Creating a campaign is only done on your DacWin customer interface.

### 2. App users

```python
from dacwinapi import AppUserService

# create an instance of AppUserService
appUserService = AppUserService(api_key="your_app_api_key")

# add new app user with referral information
app_user_created = await appUserService.create(
	reference="3ddd",
	referrer_referral_code="AAAAA"
)

print(app_user_created)

# retrieve the list of app users of the app
app_users = appUserService.getAll()

# retieve one app user by her id
app_user = appUserService.getOne(id=1) # 2 is the app user id

# retieve one app user by her reference
app_user = appUserService.getOne(reference="a2sddd") # "a2sddd" is the app user reference
```

### 3. Events

```python
from dacwinapi import EventService

# create an instance of EventService
eventService = EventService(api_key="your_app_api_key")

# add a new event for specific app user and campaign
event_created = eventService.create(
	name="ddd",
	campaign_id=18,
	app_user_id=14
)

print(event_created)

# retrieve the list of events of the app
events = eventService.getAll()

# retrieve the list of app's events of specific campaign
events = eventService.getAll(campaign_id=12)

# retrieve one event
event = eventService.getOne(12) # 12 is the event id

```

### 4. Rewards

```python
from dacwinapi import RewardService

# create an instance of RewardService
rewardService = RewardService(api_key="your_app_api_key")

# retrieve the list of rewards of the app
rewards = rewardService.getAll()

# retrieve the list of app's rewards of specific campaign
rewards = rewardService.getAll(campaign_id=12)

# retrieve one reward
reward = rewardService.getOne(id=12)
```