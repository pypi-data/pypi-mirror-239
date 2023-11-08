from googleapiclient.discovery import build
import gandai as ts
import pandas as pd

def page_one(q: str) -> pd.DataFrame:
    service = build(
        "customsearch",
        "v1",
        developerKey=ts.secrets.access_secret_version("GOOGLE_SEARCH_KEY"),
    )
    results = service.cse().list(q=q, cx="12cb7a511cc804eb0").execute()
    return pd.DataFrame(results["items"])


def search(q: str, count: int = 10) -> pd.DataFrame:
    if count > 100:
        print("max @ 100 for now")
        count = 100

    all_results = []
    for i in range(0, count, 10):
        service = build(
            "customsearch",
            "v1",
            developerKey=ts.secrets.access_secret_version("GOOGLE_SEARCH_KEY"),
        )
        results = service.cse().list(q=q, cx="12cb7a511cc804eb0", start=i).execute()
        all_results.extend(results["items"])
    df = pd.DataFrame(all_results)[["title", "link", "snippet"]]
    return df


HOW_TO_GOOGLE = """
To search Google, you will create an Event object.
Here is the dataclass:
@dataclass
class Event:
    search_uid: int  # fk # add index
    actor_key: str  # fk
    type: str  
    data: dict = field(default_factory=dict)
    id: int = field(default=None)  # pk
    # created: int = field(init=False)

List[Event] examples asdict:

[{
  'search_uid': 200,
  'domain': null,
  'actor_key': '3125740050',
  'type': 'google',
  'data': {'q': '"golf cart" AND audio'},
  'created': 1697813193},
{
  'search_uid': 5255570,
  'domain': null,
  'actor_key': '3102835279',
  'type': 'google',
  'data': {'q': '"commercial" AND "door" AND ("repair" OR "maintenance" OR "replacement") AND "new York City"'},
  'created': 1697814555}]

Your actor_key is 'chatgpt'
The type is 'google'
You will not set the id or created fields.
The default count is 10

You will return the List[Event] as adict JSON 
You will not inlcude newline characters
You will return only the JSON 
"""