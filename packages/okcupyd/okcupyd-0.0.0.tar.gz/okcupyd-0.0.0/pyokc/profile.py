import itertools

from lxml import html

from . import helpers
from . import util
from .xpath import xpb


class Question(object):

    def __init__(self, id_, text, user_answer, explanation):
        self.id = id_
        self.text = text
        self.user_answer = user_answer
        self.explanation = explanation

    def __repr__(self):
        return '<Question: {0}>'.format(self.text)


class QuestionFetcher(object):

    step = 10

    @classmethod
    def build(cls, session, username):
        return cls(QuestionHTMLFetcher(session, username), QuestionProcessor(session))

    _page_data_xpb = xpb.div.with_class('pages_data')
    _current_page_xpb = _page_data_xpb.input(id='questions_pages_page').select_attribute_('value')
    _total_page_xpb = _page_data_xpb.input(id='questions_pages_total').select_attribute_('value')

    def __init__(self, html_fetcher, processor):
        self._html_fetcher = html_fetcher
        self._processor = processor

    def _pages_left(self, tree):
        return int(self._current_page_xpb.one_(tree)) < int(self._total_page_xpb.one_(tree))

    def fetch(self, start_at=0, get_at_least=None, id_to_existing=None):
        current_offset = start_at + 1
        generators = []
        while True:
            tree = html.fromstring(self._html_fetcher.fetch(current_offset))
            generators.append(self._processor.process(tree))
            if not self._pages_left(tree):
                break
            current_offset = current_offset + self.step
        return itertools.chain(*generators)


class QuestionHTMLFetcher(object):

    def __init__(self, session, username, step=10, **additional_parameters):
        self._session = session
        self._username = username
        self.step = step
        self._additional_parameters = additional_parameters

    @property
    def _uri(self):
        return 'profile/{0}/questions'.format(self._username)

    def _query_params(self, start_at):
        parameters = {'low': start_at, 'leanmode': 1}
        parameters.update(self._additional_paramters)
        return parameters

    def fetch(self, start_at):
        response = self._session.okc_get(self._uri,
                                         params=self._query_params(start_at))
        return response.content.decode('utf8')


class QuestionProcessor(object):

    _question_xpb = xpb.div.with_class('question')

    def __init__(self, session, id_to_existing=None):
        self._session = session
        self.id_to_existing = id_to_existing or {}

    def _process_question_element(self, question_element):
        id_ = question_element.attrib['data-qid']
        text = xpb.div.with_class('qtext').p.get_text_(question_element).strip()
        answer = None
        explanation = None
        if 'not_answered' not in question_element.attrib['class']:
            answer = xpb.span.attribute_contains('id', 'answer_target').\
                     get_text_(question_element).strip()

            explanation = xpb.div.span.with_class('note').get_text_(question_element).strip()
        return Question(id_, text, answer, explanation)

    def process(self, tree):
        for question_element in self._question_xpb.apply_(tree):
                yield self._process_question_element(question_element)


class Profile(object):

    attributes = set(('username', 'id', 'age', 'location', 'match_percentage',
                      'enemy_percentage', 'rating', 'contacted'))

    def __init__(self, session, username, *args, **kwargs):
        self._session = session
        self.username = username
        self._question_fetcher = QuestionFetcher.build(session, username)
        self.questions = util.Fetchable(self._question_fetcher)

        for key, value in kwargs.items():
            setattr(self, key, value)

        self._initialize_fillable_traits()

    @util.cached_property
    def _profile_response(self):
        return self._session.get(
            'https://www.okcupid.com/profile/{0}'.format(self.username)
        ).content.decode('utf8')

    @util.cached_property
    def _profile_tree(self):
        return html.fromstring(self._profile_response)

    def message_request_parameters(self, content, thread_id):
        return {
            'ajax': 1,
            'sendmsg': 1,
            'r1': self.username,
            'body': content,
            'threadid': thread_id,
            'authcode': self.authcode,
            'reply': 1 if thread_id else 0,
            'from_profile': 1
        }

    @util.cached_property
    def authcode(self):
        return helpers.get_authcode(self._profile_response)

    @util.cached_property
    def picture_uris(self):
        pics_request = self._session.okc_get('profile/{0}/photos?cf=profile'.format(self.username))
        pics_tree = html.fromstring(pics_request.content.decode('utf8'))
        return xpb.div(id='album_0').img.select_attribute_('src', pics_tree)

    rating_xpath = xpb.ul.li.with_class('current-rating').select_attribute_('style')

    @util.cached_property
    def rating(self):
        rating_style = self.rating_xpath.one_(self._profile_tree)
        width_percentage = int(''.join(c for c in rating_style if c.isdigit()))
        return (width_percentage // 100) * 5

    @util.cached_property
    def age(self):
        return int(xpb.span(id='ajax_age').get_text_(self._profile_tree).strip())

    @util.n_partialable
    def message(self, message, thread_id=None):
        return helpers.MessageSender(self._session).send_message(self.username, message,
                                                                 self.authcode, thread_id)

    def _initialize_fillable_traits(self):
        self.pics = []
        self.questions = []
        self.traits = []
        self.essays = {
            'self summary': '',
            'life': '',
            'good at': '',
            'first things': '',
            'favorites': '',
            'six things': '',
            'thinking': '',
            'friday night': '',
            'private thing': '',
            'message me if': '',
            }
        self.looking_for = {
            'gentation': '',
            'ages': '',
            'near': '',
            'single': '',
            'seeking': '',
            }
        self.details = {
            'last online': '',
            'orientation': '',
            'ethnicity': '',
            'height': '',
            'body type': '',
            'diet': '',
            'smokes': '',
            'drinks': '',
            'drugs': '',
            'religion': '',
            'sign': '',
            'education': '',
            'job': '',
            'income': '',
            'relationship type': '',
            'offspring': '',
            'pets': '',
            'speaks': '',
            }

    def update_traits(self):
        """
        Fill `self.traits` the personality traits of this profile.
        """
        get_traits = self._session.get('http://www.okcupid.com/profile/{0}/personality'.format(self.username))
        tree = html.fromstring(get_traits.content.decode('utf8'))
        self.traits = tree.xpath("//div[@class = 'pt_row']//label/text()")

    def __repr__(self):
        return 'Profile("{0}")'.format(self.username)

