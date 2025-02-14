from queue import Queue
import asyncio
import aiohttp
from tqdm import tqdm
from bs4 import BeautifulSoup
from neomodel import config
from graph_models import Person

# Neo4j database configuration
config.DATABASE_URL = "bolt://neo4j:test1234@localhost:7687"

# Queue initialization
q = Queue(maxsize=1000)

# Occupation filters for categorization
occupation_filters = {
    "politician": ['politician', 'statesman'],
    "cricketer": ['cricket'],
    "bollywood": ["actor", "actress", "director", "singer", "producer"],
}

# Data sources for scraping
SOURCES = {
    "politician": [
        "Narendra Modi", "Rahul Gandhi", "Atal Bihari Vajpayee", "Indira Gandhi",
        "Mamata Banerjee", "Lalu Prasad Yadav", "N. Chandrababu Naidu",
        "J. Jayalalithaa", "Arvind Kejriwal", "Sharad Pawar", "Bal Thackeray",
        "Arun Jaitley"
    ],
    "bollywood": [
        "Shah Rukh Khan", "Amitabh Bachchan", "Aamir Khan", "Sanjay Dutt",
        "Rajnikanth", "Dharmendra", "Anushka Sharma", "Deepika Padukone",
        "Kangana Ranaut", "Alia Bhatt", "Naseeruddin Shah", "Kamal Hassan",
        "Saif Ali Khan", "Rishi Kapoor", "Hema Malini", "Jaya Bachchan",
        "Ritiesh Deshmukh"
    ],
    "cricketer": [
        "Sachin Tendulkar", "MS Dhoni", "Sourav Ganguly", "Virat Kohli",
        "Yuvraj Singh", "Gautam Gambhir", "Navjot Singh Sidhu", "Ravi Shastri",
        "Mohammad Azharuddin", "Rahul Dravid", "Anil Kumble", "Rohit Sharma",
        "Harbhajan Singh", "Hardik Pandya", "Rishabh Pant", "Jasprit Bumrah",
        "Kedar Jadhav", "Sanju Samson", "Mohammad Kaif", "Ajit Agarkar",
        "Sanjay Manjrekar"
    ],
}

MAX_ADDITION_SOURCES = 1000  # Increased limit
additionSourceCount = 0


async def scrape(link, curr, iterred, session):
    """Scrapes Wikipedia pages and updates the Neo4j graph."""
    global additionSourceCount
    url2 = "https://en.wikipedia.org" + str(link.get("href"))
    person_name = str(link.get("title"))

    if len(person_name.split(" ")) > 3 or person_name == curr.name or person_name in iterred:
        return None
    iterred.add(person_name)

    try:
        person_node = Person.nodes.get(name=person_name)
        tqdm.write(f'{person_name} EXISTS')
        curr.friends.connect(person_node)
        return None
    except Person.DoesNotExist:
        pass

    if additionSourceCount > MAX_ADDITION_SOURCES:
        return None

    async with session.get(url2) as resp:
        cont = await resp.text()
    soup2 = BeautifulSoup(cont, "html.parser")

    # Check if person is alive
    isAlive = True
    infobox = soup2.find("table", class_="infobox")
    if not infobox or "Born" not in infobox.get_text():
        return None
    if "Died" in infobox.get_text():
        isAlive = False

    tqdm.write(f'\n{person_name}')

    # Extract text length
    text_dict = soup2.select(".mw-parser-output > p")
    c = sum(len(para.get_text().split()) for para in text_dict)
    if c < 1500:
        return None
    tqdm.write(f'Text length is {c}')

    # Create new node
    now = Person(name=person_name)

    # Extract first paragraph
    first_para = next((para.get_text(strip=True) for para in text_dict if para.get_text(strip=True)), "")
    line = first_para.split('\n')[0]

    # Extract image from infobox using multiple possible selectors
    imagebox = soup2.select_one(".infobox-image img, .infobox img, .thumbimage")
    if imagebox and 'src' in imagebox.attrs:
        now.imgLink = f"https:{imagebox['src']}"
    else:
        # Fallback: Try to find the image in the infobox
        infobox_image = infobox.find("img")
        if infobox_image and 'src' in infobox_image.attrs:
            now.imgLink = f"https:{infobox_image['src']}"

    now.alive = isAlive
    now.pageLink = url2

    # Determine if Indian
    isIndian = "Indian" in line
    now.indian = isIndian
    if not isIndian:
        return None

    # Assign occupation based on keywords
    for occupation, keywords in occupation_filters.items():
        setattr(now, occupation, any(keyword in line for keyword in keywords))

    # Save and connect to the graph
    now.save()
    tqdm.write(f'SAVED {person_name}')
    curr.friends.connect(now)
    additionSourceCount += 1

    return person_name


async def main():
    """Main function to run the scraper and build the Neo4j graph."""
    global additionSourceCount
    async with aiohttp.ClientSession() as session:
        for category, sources in SOURCES.items():
            for source in sources:
                q.put(source)

        pbar = tqdm(total=q.qsize())

        while not q.empty():
            source = q.get()
            tqdm.write(f'\nSOURCE: {source}')
            additionSourceCount += 1

            try:
                curr = Person.nodes.get(name=source)
            except Person.DoesNotExist:
                curr = Person(name=source).save()

            URL = "https://en.wikipedia.org/wiki/" + source.replace(" ", "_")
            async with session.get(URL) as resp:
                content = await resp.text()
            soup = BeautifulSoup(content, "html.parser")
            url_dict = soup.select("p a[href]")

            iterred = set()
            try:
                names = await asyncio.gather(*[scrape(link, curr, iterred, session) for link in url_dict])
                names = [name for name in names if name]
            except Exception as e:
                tqdm.write(f"Error processing links: {e}")
                names = []

            for name in names:
                q.put(name)
                pbar.total += 1

            pbar.update(1)

        pbar.close()


if __name__ == "__main__":
    asyncio.run(main())
