from flask_frozen import Freezer
from app import app
from utils.newsLoader import loadNews, loadSingleNews
from utils.researchLoader import loadResearch
from utils.publicationLoader import loadPublications
from utils.peopleLoader import loadPeoples

freezer = Freezer(app)

# Dynamic route generators
@freezer.register_generator
def personDetail():
	for person in loadPeoples():
		yield {'slug': person['slug']}


@freezer.register_generator
def show_news():
	for news in loadNews():
		yield {'slug': news['slug']}

@freezer.register_generator
def showResearch():
	for res in loadResearch():
		yield {'slug': res['slug']}


@freezer.register_generator
def showPublication():
	for pub in loadPublications():
		yield {'slug': pub['slug']}


