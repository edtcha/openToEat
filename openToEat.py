#NOTE: Bugs may exist, API limit has been reached.

from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from metaphor_python import Metaphor

#API key setup
api_key = "METAPHOR_API_KEY"
openai.api_key = os.getenv("OPENAI_API_KEY")
metaphor = Metaphor(api_key)

#Initial query for places to eat
query = "good places to eat in SF"
#Oldest posts
oldestAge = relativedelta(years=1, months=1, days=1)
startDate = date.today()- oldestAge
#Metaphor search
search_response = metaphor.search(query, 
                                  num_results=25, 
                                  include_domains=["yelp.com", "tripadvisor.com"],
                                  start_published_date= f"{startDate.year}-{startDate.month}-{startDate.day}",
                                  use_autoprompt=True,)  

#GPT setup messages
SYSTEM_MESSAGE = "given text, note hours of operation for resturants"
USER_QUESTION = f"given hours of operation, what resturants are currently open now on: {datetime.now()}"
#Creating message list for GPT
contents_response = search_response.get_contents()
preset = [{"role": "user", "content": i} for i in contents_response.contents]
preset.insert(0, {"role": "system", "content": SYSTEM_MESSAGE})
preset.append({"role": "user", "content": USER_QUESTION})
#GPT query
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=preset,
)

#Return currently open resturants at current time
openResturants = completion.choices[0].message.content
print(f"Currently open resturants are: {openResturants}")
