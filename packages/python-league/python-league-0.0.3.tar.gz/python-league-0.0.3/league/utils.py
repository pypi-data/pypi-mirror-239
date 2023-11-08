import requests


class DataDragon:
    """
    Currently in python-league, it only supports '/ko_KR/champion.json'

    **It is not always updated immediately after a patch according to Riot Games.**
    """
    def __init__(self) -> None:
        self.base_url = "https://ddragon.leagueoflegends.com/cdn/"
        self.version = "13.12.1"

    def champion_data(self):
        data = requests.get(self.base_url+self.version+"/data/ko_KR/champion.json")
       
        return data.json()


class UrlHandler:
    def __init__(self, api_key) -> None:
        self._api_key = api_key
        self._request_headers = {
            "X-Riot-Token": self.api_key
        }
    
    @property
    def api_key(self):
        """
        Get: api_key
        """
        return self._api_key
 
    def request(self, url, params=None):
        res = requests.get(
            url=url,
            headers=self._request_headers,
            params=params
        )
        res.raise_for_status()

        return res.json()

