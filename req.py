import requests
from datetime import datetime


payload = {
    "user_id": "123456789",
    "username": "example_user",
    "guild_id": "987654321",
    "channel_id": "1122334455",
    "message_id": "5566778899",
    "user_message": """Kendrick Lamar Duckworth (born June 17, 1987) is an American rapper. Regarded as one of the greatest rappers of all time, he was awarded the 2018 Pulitzer Prize for Music, becoming the first musician outside of the classical and jazz genres to receive the honor.
Born in Compton, California, Lamar began releasing music under the stage name K.Dot while attending high school. He signed with Top Dawg Entertainment (TDE) in 2005, and co-founded the hip hop supergroup Black Hippy there. Following the 2011 release of his alternative rap debut album Section.80, Lamar secured a joint contract with Dr. Dre's Aftermath Entertainment and Interscope Records. He rose to prominence with his gangsta rap-influenced second album Good Kid, M.A.A.D City (2012), which became the longest-charting hip hop studio album in Billboard 200 history; Rolling Stone named it the greatest concept album of all time. In 2015, Lamar scored his first Billboard Hot 100 number-one single, after featuring on the remix of Taylor Swift's "Bad Blood", and released his third album, To Pimp a Butterfly, which infused hip-hop with historical African-American music genres such as jazz, funk, and soul, and became his first of six consecutive number-one albums on the Billboard 200 chart.""",
    "timestamp": datetime.now().isoformat(),
    "intent": "biography_info",
    "prompt_type": "informational",
    "status": "pending",
}

# Send the request to the server
response = requests.post("http://localhost:8000/api/ask", json=payload)

# Print the server's response
if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.status_code, response.text)
