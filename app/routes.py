from flask import render_template, request, redirect, url_for, abort, Response
from utils.newsLoader import loadNews, loadSingleNews
from utils.researchLoader import loadResearch
from utils.publicationLoader import loadPublications
from utils.peopleLoader import loadPeoples
from collections import defaultdict
import datetime

from app import app
app.config['PREFERRED_URL_SCHEME'] = 'https'
app.config['SERVER_NAME'] = 'biovism.ugent.be'


@app.route('/')
def index():
    groupNews = loadNews()[:5]
    return render_template('index.html', news=groupNews)


@app.route('/people/')
def people():
    items = loadPeoples()
    roles = ["Principal Investigators", "Post-docs", "In-house Staff", "Affiliate Staff", "Alumni"]
    groupedPeople = defaultdict(list)
    for person in items:
        groupedPeople[person["group"]].append(person)
    return render_template("peopleMain.html", groupedPeople=groupedPeople, roles=roles)


@app.route('/people/<slug>/')
def personDetail(slug):
    items = loadPeoples()
    item = None
    for i in items:
        if i["slug"] == slug:
            item = i
            item['degrees'] = reversed(eval(item['degrees']))
            item['interests'] = eval(item['interests'])
            item['profile'] = eval(item['profile'])

    p = loadPublications()
    publication = []
    item["publications"] = eval(item["publications"])
    for i in item["publications"]:
        x = None
        for j in p:
            if j["slug"] == i:
                x = j
        publication.append(x)

    return render_template('person.html', person=item, publications=publication)


@app.route('/research/')
def research():
    items = loadResearch()
    return render_template("researchMain.html", research=items)


@app.route("/research/<slug>/")
def showResearch(slug):
    items = loadResearch()
    item = None
    for i in items:
        if i["slug"] == slug:
            item = i
    if not item:
        abort(404)

    p = loadPeoples()
    researcher = []
    item["people"] = eval(item["people"])
    for i in item["people"]:
        x = None
        for j in p:
            if j["slug"] == i:
                x = j
                x['degrees'] = reversed(eval(x['degrees']))
                x['interests'] = eval(x['interests'])
                x['profile'] = eval(x['profile'])
        researcher.append(x)

    p = loadPublications()
    publication = []
    item["publications"] = eval(item["publications"])
    for i in item["publications"]:
        x = None
        for j in p:
            if j["slug"] == i:
                x = j
        publication.append(x)

    return render_template("research.html", item=item, researchers=researcher, publications=publication)


@app.route('/publications/')
def publications():
    items = loadPublications()
    items.sort(key=lambda x: (x.get("year", 0), x.get("date", "")), reverse=True)

    grouped = {}
    for pub in items:
        year = pub.get("year")
        if year not in grouped:
            grouped[year] = []
        grouped[year].append(pub)
    return render_template("publicationMain.html", grouped=grouped)


@app.route("/publication/<slug>/")
def showPublication(slug):
    items = loadPublications()
    item = None
    for i in items:
        if i["slug"] == slug:
            item = i
    if not item:
        abort(404)
    return render_template("publication.html", publication=item)


@app.route('/news/')
def news():
    all_news = loadNews()
    return render_template('newsMain.html', news=all_news)


@app.route('/news/<slug>/')
def show_news(slug):
    item = loadSingleNews(slug)
    if not item:
        return "News item not found", 404
    return render_template('news.html', item=item)


@app.route("/join/")
def join():
    return render_template("join.html")


@app.route("/sitemap.xml", methods=["GET"])
def sitemap():
    pages = []
    lastmod = datetime.datetime.now().date().isoformat()

    # Static pages
    static_routes = ['index', 'people', 'research', 'news', 'publications', 'join']
    for route in static_routes:
        pages.append({
            "loc": url_for(route, _external=True),
            "lastmod": lastmod
        })

    # People detail pages
    for item in loadPeoples():
        pages.append({
            "loc": url_for('personDetail', slug=item['slug'], _external=True),
            "lastmod": lastmod
        })

    # News detail pages
    for item in loadNews():
        pages.append({
            "loc": url_for('show_news', slug=item['slug'], _external=True),
            "lastmod": lastmod
        })

    # Research detail pages
    for item in loadResearch():
        pages.append({
            "loc": url_for('showResearch', slug=item['slug'], _external=True),
            "lastmod": lastmod
        })

    # Publication detail pages
    for item in loadPublications():
        pages.append({
            "loc": url_for('showPublication', slug=item['slug'], _external=True),
            "lastmod": lastmod
        })

    # Render XML
    sitemap_xml = render_template("sitemap.xml", pages=pages)
    return Response(sitemap_xml, mimetype="text/xml")


@app.route('/robots.txt')
def robots():
    return Response(
        "User-agent: *\nDisallow:\nSitemap: https://biovism.ugent.be/sitemap.xml",
        mimetype="text/plain")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
