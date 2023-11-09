# python-league
Python-league helps you to use League of Legends API.

## Installation
```
pip install python-league --upgrade
```

## How to use
```python
from league import LeagueAPI

lol = LeagueAPI(api_key="Your API KEY")

# 소환사 정보 가져오기
summoner = lol.get_summoner(summoner_name="summoner name")

# 소환사의 챔피언 숙련도 불러오기
champion_mastery = summoner.get_all_champion_mastery() #champion mastery list of *summoner*

# 챔피언 정보 불러오기
# 1. id로 불러오기
champion = lol.get_champion_by_id(championID="champion id")
# 2. 이름으로 불러오기(en)
champion = lol.get_champion_by_name("Aatrox") # 아트록스

print(champion)
```