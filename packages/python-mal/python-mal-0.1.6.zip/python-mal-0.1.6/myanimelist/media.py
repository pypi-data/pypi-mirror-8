#!/usr/bin/python
# -*- coding: utf-8 -*-

import abc
import bs4
import decimal
import re

import utilities
from base import Base, Error, loadable

class MalformedMediaPageError(Error):
  def __init__(self, media_id, html, message=None):
    super(MalformedMediaPageError, self).__init__(message=message)
    self.media_id = int(media_id)
    if isinstance(html, unicode):
      self.html = html
    else:
      self.html = str(html).decode(u'utf-8')
  def __str__(self):
    return "\n".join([
      super(MalformedMediaPageError, self).__str__(),
      "ID: " + unicode(self.media_id),
      "HTML: " + self.html
    ]).encode(u'utf-8')

class InvalidMediaError(Error):
  def __init__(self, media_id, message=None):
    super(InvalidMediaError, self).__init__(message=message)
    self.media_id = media_id
  def __str__(self):
    return "\n".join([
      super(InvalidMediaError, self).__str__(),
      "ID: " + unicode(self.media_id)
    ])

class Media(Base):
  """
    Base class for all media resources on MAL.
  """
  __metaclass__ = abc.ABCMeta

  # a container of status terms for this media.
  # keys are status ints, values are statuses e.g. "Airing"
  @abc.abstractproperty
  def status_terms(self):
    pass

  # a string, containing the verb used to consume this media, e.g. "read"
  @abc.abstractproperty
  def consuming_verb(self):
    pass

  def __init__(self, session, id):
    super(Media, self).__init__(session)
    self.id = id
    if not isinstance(self.id, int) or int(self.id) < 1:
      raise InvalidMediaError(self.id)
    self._title = None
    self._picture = None
    self._alternative_titles = None
    self._type = None
    self._status = None
    self._genres = None
    self._score = None
    self._rank = None
    self._popularity = None
    self._members = None
    self._favorites = None
    self._popular_tags = None
    self._synopsis = None
    self._related = None
    self._characters = None
    self._score_stats = None
    self._status_stats = None

  def parse_sidebar(self, media_page):
    """
      Given a BeautifulSoup object containing MAL media page's DOM, returns a dict with this media's attributes found on the sidebar.
    """
    media_info = {}

    # if MAL says the series doesn't exist, raise an InvalidMediaError.
    error_tag = media_page.find(u'div', {'class': 'badresult'})
    if error_tag:
        raise InvalidMediaError(self.id)

    title_tag = media_page.find(u'div', {'id': 'contentWrapper'}).find(u'h1')
    if not title_tag.find(u'div'):
      # otherwise, raise a MalformedMediaPageError.
      raise MalformedMediaPageError(self.id, media_page, message="Could not find title div")

    utilities.extract_tags(title_tag.find_all())
    media_info[u'title'] = title_tag.text.strip()

    info_panel_first = media_page.find(u'div', {'id': 'content'}).find(u'table').find(u'td')

    picture_tag = info_panel_first.find(u'img')
    media_info[u'picture'] = picture_tag.get(u'src').decode('utf-8')

    # assemble alternative titles for this series.
    media_info[u'alternative_titles'] = {}
    alt_titles_header = info_panel_first.find(u'h2', text=u'Alternative Titles')
    if alt_titles_header:
      next_tag = alt_titles_header.find_next_sibling(u'div', {'class': 'spaceit_pad'})
      while True:
        if next_tag is None or not next_tag.find(u'span', {'class': 'dark_text'}):
          # not a language node, break.
          break
        # get language and remove the node.
        language = next_tag.find(u'span').text[:-1]
        utilities.extract_tags(next_tag.find_all(u'span', {'class': 'dark_text'}))
        names = next_tag.text.strip().split(u', ')
        media_info[u'alternative_titles'][language] = names
        next_tag = next_tag.find_next_sibling(u'div', {'class': 'spaceit_pad'})

    type_tag = info_panel_first.find(text=u'Type:').parent.parent
    utilities.extract_tags(type_tag.find_all(u'span', {'class': 'dark_text'}))
    media_info[u'type'] = type_tag.text.strip()

    status_tag = info_panel_first.find(text=u'Status:').parent.parent
    utilities.extract_tags(status_tag.find_all(u'span', {'class': 'dark_text'}))
    media_info[u'status'] = status_tag.text.strip()

    genres_tag = info_panel_first.find(text=u'Genres:').parent.parent
    utilities.extract_tags(genres_tag.find_all(u'span', {'class': 'dark_text'}))
    media_info[u'genres'] = []
    for genre_link in genres_tag.find_all('a'):
      link_parts = genre_link.get('href').split('[]=')
      # of the form /anime|manga.php?genre[]=1
      genre = self.session.genre(int(link_parts[1])).set({'name': genre_link.text})
      media_info[u'genres'].append(genre)

    # grab statistics for this media.
    score_tag = info_panel_first.find(text=u'Score:').parent.parent
    # get score and number of users.
    users_node = [x for x in score_tag.find_all(u'small') if u'scored by' in x.text][0]
    num_users = int(users_node.text.split(u'scored by ')[-1].split(u' users')[0])
    utilities.extract_tags(score_tag.find_all())
    media_info[u'score'] = (decimal.Decimal(score_tag.text.strip()), num_users)

    rank_tag = info_panel_first.find(text=u'Ranked:').parent.parent
    utilities.extract_tags(rank_tag.find_all())
    media_info[u'rank'] = int(rank_tag.text.strip()[1:].replace(u',', ''))

    popularity_tag = info_panel_first.find(text=u'Popularity:').parent.parent
    utilities.extract_tags(popularity_tag.find_all())
    media_info[u'popularity'] = int(popularity_tag.text.strip()[1:].replace(u',', ''))

    members_tag = info_panel_first.find(text=u'Members:').parent.parent
    utilities.extract_tags(members_tag.find_all())
    media_info[u'members'] = int(members_tag.text.strip().replace(u',', ''))

    favorites_tag = info_panel_first.find(text=u'Favorites:').parent.parent
    utilities.extract_tags(favorites_tag.find_all())
    media_info[u'favorites'] = int(favorites_tag.text.strip().replace(u',', ''))

    # get popular tags.
    tags_header = media_page.find(u'h2', text=u'Popular Tags')
    tags_tag = tags_header.find_next_sibling(u'span')
    media_info[u'popular_tags'] = {}
    for tag_link in tags_tag.find_all('a'):
      tag = self.session.tag(tag_link.text)
      num_people = int(re.match(r'(?P<people>[0-9]+) people', tag_link.get('title')).group('people'))
      media_info[u'popular_tags'][tag] = num_people

    return media_info

  def parse(self, media_page):
    """
      Given a BeautifulSoup object containing a MAL media page's DOM, returns a dict with this media's attributes.
    """
    media_info = self.parse_sidebar(media_page)

    synopsis_elt = media_page.find(u'h2', text=u'Synopsis').parent
    utilities.extract_tags(synopsis_elt.find_all(u'h2'))
    media_info[u'synopsis'] = synopsis_elt.text.strip()

    related_title = media_page.find(u'h2', text=u'Related ' + self.__class__.__name__)
    if related_title:
      related_elt = related_title.parent
      utilities.extract_tags(related_elt.find_all(u'h2'))
      related = {}
      for link in related_elt.find_all(u'a'):
        href = link.get(u'href').replace(u'http://myanimelist.net', '')
        if not re.match(r'/(anime|manga)', href):
          break
        curr_elt = link.previous_sibling
        if curr_elt is None:
          # we've reached the end of the list.
          break
        related_type = None
        while True:
          if not curr_elt:
            raise MalformedAnimePageError(self.id, related_elt, message="Prematurely reached end of related anime listing")
          if isinstance(curr_elt, bs4.NavigableString):
            type_match = re.match(u'(?P<type>[a-zA-Z\ \-]+):', curr_elt)
            if type_match:
              related_type = type_match.group(u'type')
              break
          curr_elt = curr_elt.previous_sibling
        title = link.text
        # parse link: may be manga or anime.
        href_parts = href.split(u'/')
        # sometimes links on MAL are broken, of the form /anime//
        if href_parts[2] == '':
          continue
        # of the form: /(anime|manga)/1/Cowboy_Bebop
        obj_id = int(href_parts[2])
        new_obj = getattr(self.session, href_parts[1])(obj_id).set({'title': title})
        if related_type not in related:
          related[related_type] = [new_obj]
        else:
          related[related_type].append(new_obj)
      media_info[u'related'] = related
    else:
      media_info[u'related'] = None
    return media_info

  def parse_stats(self, anime_page):
    """
      Given a BeautifulSoup object containing a MAL media stats page's DOM, returns a dict with this media's attributes.
    """
    media_info = self.parse_sidebar(media_page)
    verb_progressive = self.consuming_verb + u'ing'
    status_stats = {
      verb_progressive: 0,
      'completed': 0,
      'on_hold': 0,
      'dropped': 0,
      'plan_to_' + self.consuming_verb: 0
    }
    consuming_elt = media_page.find(u'span', {'class': 'dark_text'}, text=verb_progressive.capitalize())
    if consuming_elt:
      status_stats[verb_progressive] = int(consuming_elt.nextSibling.strip().replace(u',', ''))

    completed_elt = media_page.find(u'span', {'class': 'dark_text'}, text="Completed:")
    if completed_elt:
      status_stats[u'completed'] = int(completed_elt.nextSibling.strip().replace(u',', ''))

    on_hold_elt = media_page.find(u'span', {'class': 'dark_text'}, text="On-Hold:")
    if on_hold_elt:
      status_stats[u'on_hold'] = int(on_hold_elt.nextSibling.strip().replace(u',', ''))

    dropped_elt = media_page.find(u'span', {'class': 'dark_text'}, text="Dropped:")
    if dropped_elt:
      status_stats[u'dropped'] = int(dropped_elt.nextSibling.strip().replace(u',', ''))

    planning_elt = media_page.find(u'span', {'class': 'dark_text'}, text="Plan to " + self.consuming_verb.capitalize() + ":")
    if planning_elt:
      status_stats[u'plan_to_' + self.consuming_verb] = int(planning_elt.nextSibling.strip().replace(u',', ''))
    media_info[u'status_stats'] = status_stats

    score_stats_header = media_page.find(u'h2', text='Score Stats')
    score_stats = {
      1: 0,
      2: 0,
      3: 0,
      4: 0,
      5: 0,
      6: 0,
      7: 0,
      8: 0,
      9: 0,
      10: 0
    }
    if score_stats_header:
      score_stats_table = score_stats_header.find_next_sibling(u'table')
      if score_stats_table:
        score_stats = {}
        score_rows = score_stats_table.find_all(u'tr')
        for i in xrange(len(score_rows)):
          score_value = int(score_rows[i].find(u'td').text)
          score_stats[score_value] = int(score_rows[i].find(u'small').text.replace(u'(u', '').replace(u' votes)', ''))
    media_info[u'score_stats'] = score_stats

    return media_info

  def parse_characters(self, character_page):
    """
      Given a BeautifulSoup object containing a MAL media's character page DOM, return a dict with this media's character attributes.
    """
    media_info = self.parse_sidebar(character_page)
    character_title = filter(lambda x: u'Characters' in x.text, character_page.find_all(u'h2'))
    media_info[u'characters'] = {}
    if character_title:
      character_title = character_title[0]
      curr_elt = character_title.find_next_sibling(u'table')
      while curr_elt:
        curr_row = curr_elt.find(u'tr')
        # character in second col.
        character_col = curr_row.find_all(u'td', recursive=False)[1]
        character_link = character_col.find(u'a')
        character_name = ' '.join(reversed(character_link.text.split(u', ')))
        link_parts = character_link.get(u'href').split(u'/')
        # of the form /character/7373/Holo
        character = self.session.character(int(link_parts[2])).set({'name': character_name})
        role = character_col.find(u'small').text
        media_info[u'characters'][character] = {'role': role}
        curr_elt = curr_elt.find_next_sibling(u'table')
    return media_info

  def load(self):
    """
      Fetches the MAL media page and sets the current media's attributes.
    """
    media_page = self.session.session.get(u'http://myanimelist.net/' + self.__class__.__name__.lower() + u'/' + str(self.id)).text
    self.set(self.parse(utilities.get_clean_dom(media_page)))
    return self

  def load_stats(self):
    """
      Fetches the MAL media stats page and sets the current media's attributes.
    """
    stats_page = self.session.session.get(u'http://myanimelist.net/' + self.__class__.__name__.lower() + u'/' + str(self.id) + u'/' + utilities.urlencode(self.title) + u'/stats').text
    self.set(self.parse_stats(utilities.get_clean_dom(stats_page)))
    return self

  def load_characters(self):
    """
      Fetches the MAL media's characters page and sets the current media's attributes.
    """
    characters_page = self.session.session.get(u'http://myanimelist.net/' + self.__class__.__name__.lower() + u'/' + str(self.id) + u'/' + utilities.urlencode(self.title) + u'/characters').text
    self.set(self.parse_characters(utilities.get_clean_dom(characters_page)))
    return self

  @property
  @loadable(u'load')
  def title(self):
    return self._title

  @property
  @loadable(u'load')
  def picture(self):
    return self._picture

  @property
  @loadable(u'load')
  def alternative_titles(self):
    return self._alternative_titles

  @property
  @loadable(u'load')
  def type(self):
    return self._type

  @property
  @loadable(u'load')
  def status(self):
    return self._status

  @property
  @loadable(u'load')
  def genres(self):
    return self._genres

  @property
  @loadable(u'load')
  def score(self):
    return self._score

  @property
  @loadable(u'load')
  def rank(self):
    return self._rank

  @property
  @loadable(u'load')
  def popularity(self):
    return self._popularity

  @property
  @loadable(u'load')
  def members(self):
    return self._members

  @property
  @loadable(u'load')
  def favorites(self):
    return self._favorites

  @property
  @loadable(u'load')
  def popular_tags(self):
    return self._popular_tags
  
  @property
  @loadable(u'load')
  def synopsis(self):
    return self._synopsis

  @property
  @loadable(u'load')
  def related(self):
    return self._related

  @property
  @loadable(u'load_characters')
  def characters(self):
    return self._characters

  @property
  @loadable(u'load_stats')
  def status_stats(self):
    return self._status_stats

  @property
  @loadable(u'load_stats')
  def score_stats(self):
    return self._score_stats