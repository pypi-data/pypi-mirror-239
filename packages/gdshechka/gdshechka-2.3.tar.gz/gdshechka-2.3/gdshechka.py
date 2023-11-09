from requests_html import HTMLSession
from bs4 import BeautifulSoup

session = HTMLSession()


def FindLevelByName(name: str) -> dict:
    """
    returns level ID by its name
    """
    findpage = session.get('https://gdbrowser.com/api/search/' + name + '?').json()
    return findpage


class Level:
    """
    Find you level by ID
    """

    def __init__(self, LevelID: int) -> dict:
        try:
            apicall = session.get('https://gdbrowser.com/api/level/' + str(LevelID)).json()
            self.api = apicall
            self.name = apicall["name"]
            self.id = apicall["id"]
            self.description = apicall["description"]
            self.description = apicall["author"]
            self.playerID = apicall["playerID"]
            self.accountID = apicall["accountID"]
            self.difficulty = apicall["difficulty"]
            self.downloads = apicall["downloads"]
            self.likes = apicall["likes"]
            self.disliked = apicall["disliked"]
            self.length = apicall["length"]
            self.stars = apicall["stars"]
            self.orbs = apicall["orbs"]
            self.diamonds = apicall["diamonds"]
            self.featured = apicall["featured"]
            self.epic = apicall["epic"]
            self.gameVersion = apicall["gameVersion"]
            self.editorTime = apicall["editorTime"]
            self.totalEditorTime = apicall["totalEditorTime"]
            self.version = apicall["version"]
            self.copiedID = apicall["copiedID"]
            self.twoPlayer = apicall["twoPlayer"]
            self.officialSong = apicall["officialSong"]
            self.customSong = apicall["customSong"]
            self.coins = apicall["coins"]
            self.verifiedCoins = apicall["verifiedCoins"]
            self.starsRequested = apicall["starsRequested"]
            self.ldm = apicall["ldm"]
            self.objects = apicall["objects"]
            self.large = apicall["large"]
            self.cp = apicall["cp"]
            self.difficultyFace = apicall["difficultyFace"]
            self.songName = apicall["songName"]
            self.songAuthor = apicall["songAuthor"]
            self.songSize = apicall["songSize"]
            self.songID = apicall["songID"]
            if 'songLink' in apicall.keys():
                self.songLink = apicall["songLink"]
            else:
                self.songLink = None
        except:
            return None

    def Comments(self):
        """Retrieves level comments"""
        comments = session.get(f'https://gdbrowser.com/api/comments/{self.id}?count=10000000').json

        return comments


class Account:
    """Search for an account by its name / account ID"""

    def __init__(self, User: str or int) -> dict:
        AccPage = session.get("https://gdbrowser.com/u/" + str(User)).text
        soup = BeautifulSoup(AccPage, 'lxml')
        self.Page = AccPage
        self.Name = soup.find_all('span')[0].text
        self.stars = soup.find_all('span')[1].text
        self.diamonds = soup.find_all('span')[2].text
        self.coins = soup.find_all('span')[3].text
        self.usercoins = soup.find_all('span')[4].text
        self.demons = soup.find_all('span')[5].text
        self.cp = soup.find_all('span')[7].text
        self.top = int(soup.find_all('p')[4].text)
        AIDandUID = soup.find_all(class_="profilePostHide")[4].text
        AIDandUID = "".join("".join(AIDandUID.split('Player ID:')).split('\nAccount ID: ')[1]).split('\n')[0]
        AIDandUID = AIDandUID.split(' ')
        self.accountID = AIDandUID[0]
        self.playerID = AIDandUID[1]

    def Comments(self) -> dict:
        """Returns comments from the page"""
        CommentsPage = session.get(f"https://gdbrowser.com/api/comments/{self.accountID}?type=profile&count=10000000").json()
        return CommentsPage