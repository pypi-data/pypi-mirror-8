import re

import six

from okcupyd import util


class maps(six.with_metaclass(util.GetAttrGetItem)):

    bodytype = util.IndexedREMap(
        'rather not say', 'thin', 'overweight', 'skinny', 'average', 'fit',
        'athletic', 'jacked', 'a little extra', 'curvy', 'full figured',
        'used up'
    )

    orientation = util.IndexedREMap('straight', 'gay', 'bisexual')

    smoking = util.IndexedREMap(
        'yes', 'sometimes', 'when drinking', 'trying to quit', 'no'
    )

    drugs = util.IndexedREMap('never', 'sometimes', 'often',
                              default=3, offset=0)

    drinking = util.IndexedREMap('very often', 'often', 'socially', 'rarely',
                                 'desperately', 'not at all')

    ethnicities = util.IndexedREMap(
        'asian', 'middle eastern', 'black', 'native american', 'indian',
        'pacific islander', ('hispanic', 'latin'), 'white', 'other'
    )

    job = util.IndexedREMap(
        'student', ('art', 'music', 'writing'), ('banking', 'finance'),
        'administration', 'technology', 'construction', 'education',
        ('entertainment', 'media'), 'management', 'hospitality', 'law',
        'medicine', 'military', ('politics', 'government'),
        ('sales', 'marketing'), ('science', 'engineering'),
        'transportation', 'unemployed', 'other', 'rather not say',
        'retired'
    )

    status = util.IndexedREMap(
        'single', 'seeing someone', 'married', 'in an open relationship'
    )

    monogamous = util.IndexedREMap('(:?[^\-]monogamous)|(:?^monogamous)',
                                   'non-monogamous')
    strictness = util.IndexedREMap('mostly', 'strictly')

    # Doesn't want kids is index 6 for some reason.
    has_kids = util.IndexedREMap('has a kid', 'has kids', (), (), (),
                                 "doesn't have kids")
    wants_kids = util.IndexedREMap('might want', 'wants', "doesn't want")

    education_status = util.IndexedREMap('graduated', 'working', 'dropped out',
                                         default=0)
    education_level = util.IndexedREMap(
        'high ?school', 'two[- ]year college', 'university', 'college',
        'masters program', 'law school', 'med school', 'ph.d program',
        'space camp'
    )

    religion = util.IndexedREMap('agnosticism', 'atheism', 'christianity',
                                 'judaism', 'catholicism', 'islam', 'hinduism',
                                 'buddhism', 'other', default=1, offset=2)
    seriousness = util.IndexedREMap('very serious', 'somewhat serious',
                                    'not too serious', 'laughing')

    sign = util.IndexedREMap(
        'aquarius', 'pisces', 'aries', 'taurus', 'gemini', 'cancer', 'leo',
        'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn',
    )
    importance = util.IndexedREMap(
        "doesn't matter", "matters alot", "fun to think about"
    )

    dogs = util.REMap.from_string_pairs(
        (('dislikes dogs', 3), ('has dogs', 1), ('likes dogs', 2)),
        default=0
    )
    cats = util.REMap.from_string_pairs(
        (('dislikes cats', 3), ('has cats', 1), ('likes cats', 2)),
        default=0
    )
    language_level = util.IndexedREMap('fluently', 'okay', 'poorly')

    diet_strictness = util.IndexedREMap('[Mm]ostly', '[Ss]trictly')

    diet_type = util.IndexedREMap('anything', 'vegetarian', 'vegan',
                                  'kosher', 'halal', 'other')
    income = util.IndexedREMap(
        'less than $20,000', '$20,000-$30,000', '$30,000-$40,000',
        '$40,000-$50,000', '$50,000-$60,000', '$60,000-$70,000',
        '$70,000-$80,000', '$80,000-$100,000', '$100,000-$150,000',
        '$150,000-$250,000', '$250,000-$500,000', '$500,000-$1,000,000',
        'More than $1,000,000'
    )


class MappingUpdater(object):

    def __init__(self, mapping):
        self.mapping = mapping

    def __call__(self, id_name, value):
        if isinstance(value, six.string_types):
            value = value.lower() # :/
        return {id_name: self.mapping[value]}


class SimpleFilterBuilder(object):

    def __init__(self, filter_number, mapping, offset=0):
        self.filter_number = filter_number
        self.mapping = mapping

    def get_number(self, values):
        acc = 0
        for value in values:
            acc += 2 ** int(self.mapping[value])
        return acc

    def get_filter(self, values):
        return '{0},{1}'.format(self.filter_number, self.get_number(values))

    __call__ = get_filter


class filters(six.with_metaclass(util.GetAttrGetItem)):

    smokes = SimpleFilterBuilder(11, maps.smoking)
    drinking = SimpleFilterBuilder(12, maps.drinking)
    drugs = SimpleFilterBuilder(13, maps.drugs)
    education = SimpleFilterBuilder(19, maps.education_level)
    job = SimpleFilterBuilder(15, maps.job)
    income = SimpleFilterBuilder(14, maps.income)
    religion = SimpleFilterBuilder(8, maps.religion)
    monogamy = SimpleFilterBuilder(73, maps.monogamous)
    diet = SimpleFilterBuilder(54, maps.diet_type)
    sign = SimpleFilterBuilder(21, maps.sign)
    ethnicity = SimpleFilterBuilder(9, maps.ethnicities)



sep_replacements = ('\\', '/', '.', '-', ' ', '$', ',', '(', ')')


gentation_to_number = {
    'girls who like guys': '34',
    'guys who like girls': '17',
    'girls who like girls': '40',
    'guys who like guys': '20',
    'both who like bi guys': '54',
    'both who like bi girls': '57',
    'straight girls only': '2',
    'straight guys only': '1',
    'gay girls only': '8',
    'gay guys only': '4',
    'bi girls only': '32',
    'bi guys only': '16',
    'bi guys and girls': '48',
    'everybody': '63',
    '': '63'
}


looking_for_re_numbers = ((re.compile("[Ff]riends"), 1),
                          (re.compile("[Ll]ong.*[Dd]ating"), 2),
                          (re.compile("[Ss]hort.*[Dd]ating"), 3),
                          (re.compile("[Ss]ex"), 6))


has_kids = {
    "has a kid": {"addition": 33686018, "power": 1},
    "has kids": {"addition": 67372036, "power": 2},
    "doesn't have kids": {"addition": 1077952576, "power": 6},
}


wants_kids = {
    "might want kids": {"addition": 18176, "power": 8},
    "wants kids": {"addition": 4653056, "power": 16},
    "doesn't want kids": {"addition": 1191182384, "power": 24},
}


language_map = {
    'Afrikaans': '2',
    'Albanian': '3',
    'Ancient Greek': '27',
    'Arabic': '4',
    'Armenian': '76',
    'Basque': '5',
    'Belarusan': '6',
    'Bengali': '7',
    'Breton': '8',
    'Bulgarian': '9',
    'C++': '71',
    'Catalan': '10',
    'Cebuano': '11',
    'Chechen': '12',
    'Chinese': '13',
    'Croatian': '14',
    'Czech': '15',
    'Danish': '16',
    'Dutch': '17',
    'English': '74',
    'Esperanto': '18',
    'Estonian': '19',
    'Farsi': '20',
    'Finnish': '21',
    'French': '22',
    'Frisian': '23',
    'Georgian': '24',
    'German': '25',
    'Greek': '26',
    'Gujarati': '77',
    'Hawaiian': '28',
    'Hebrew': '29',
    'Hindi': '75',
    'Hungarian': '30',
    'Icelandic': '31',
    'Ilongo': '32',
    'Indonesian': '33',
    'Irish': '34',
    'Italian': '35',
    'Japanese': '36',
    'Khmer': '37',
    'Korean': '38',
    'LISP': '72',
    'Latin': '39',
    'Latvian': '40',
    'Lithuanian': '41',
    'Malay': '42',
    'Maori': '43',
    'Mongolian': '44',
    'Norwegian': '45',
    'Occitan': '46',
    'Other': '73',
    'Persian': '47',
    'Polish': '48',
    'Portuguese': '49',
    'Romanian': '50',
    'Rotuman': '51',
    'Russian': '52',
    'Sanskrit': '53',
    'Sardinian': '54',
    'Serbian': '55',
    'Sign Language': '1',
    'Slovak': '56',
    'Slovenian': '57',
    'Spanish': '58',
    'Swahili': '59',
    'Swedish': '60',
    'Tagalog': '61',
    'Tamil': '62',
    'Thai': '63',
    'Tibetan': '64',
    'Turkish': '65',
    'Ukrainian': '66',
    'Urdu': '67',
    'Vietnamese': '68',
    'Welsh': '69',
    'Yiddish': '70',
}


language_map_2 = {
    'afrikaans': 'af',
    'albanian': 'sq',
    'arabic': 'ar',
    'armenian': 'hy',
    'basque': 'eu',
    'belarusan': 'be',
    'bengali': 'bn',
    'breton': 'br',
    'bulgarian': 'bg',
    'catalan': 'ca',
    'cebuano': '11',
    'chechen': 'ce',
    'chinese': 'zh',
    'c++': '71',
    'croatian': 'hr',
    'czech': 'cs',
    'danish': 'da',
    'dutch': 'nl',
    'english': 'en',
    'esperanto': 'eo',
    'estonian': 'et',
    'farsi': '20',
    'finnish': 'fi',
    'french': 'fr',
    'frisian': '23',
    'georgian': '24',
    'german': 'de',
    'greek': 'el',
    'gujarati': 'gu',
    'ancient greek': '27',
    'hawaiian': '28',
    'hebrew': 'he',
    'hindi': 'hi',
    'hungarian': 'hu',
    'icelandic': 'is',
    'ilongo': '32',
    'indonesian': 'id',
    'irish': 'ga',
    'italian': 'it',
    'japanese': 'ja',
    'khmer': '37',
    'korean': 'ko',
    'latin': 'la',
    'latvian': 'lv',
    'lisp': '72',
    'lithuanian': 'lt',
    'malay': 'ms',
    'maori': 'mi',
    'mongolian': 'mn',
    'norwegian': 'no',
    'occitan': 'oc',
    'other': '73',
    'persian': 'fa',
    'polish': 'pl',
    'portuguese': 'pt',
    'romanian': 'ro',
    'rotuman': '51',
    'russian': 'ru',
    'sanskrit': 'sa',
    'sardinian': '54',
    'serbian': 'sr',
    'sign language': '1',
    'slovak': 'sk',
    'slovenian': 'sl',
    'spanish': 'es',
    'swahili': 'sw',
    'swedish': 'sv',
    'tagalog': 'tl',
    'tamil': 'ta',
    'thai': 'th',
    'tibetan': 'bo',
    'turkish': 'tr',
    'ukrainian': 'uk',
    'urdu': 'ur',
    'vietnamese': 'vi',
    'welsh': 'cy',
    'yiddish': 'yi'
}


binary_lists = {
    'smokes': ['11', 'yes', 'sometimes', 'when drinking', 'trying to quit', 'no'],
    'drinks': ['12', 'very often', 'often', 'socially', 'rarely', 'desperately',
               'not at all'],
    'drugs': ['13', 'never', 'sometimes', 'often'],
    'education': ['19', 'high school', 'two-year college', 'college/university',
                  'masters program', 'law school', 'medical school',
                  'ph.d program'],
    'job': ['15', 'student', 'art / music / writing', 'banking / finance',
            'administration', 'technology', 'construction', 'education',
            'entertainment / media', 'management', 'hospitality', 'law',
            'medicine', 'military', 'politics / government',
            'sales / marketing', 'science / engineering', 'transporation',
            'retired'],
    'income': ['14', 'less than $20,000', '$20,000-$30,000', '$30,000-$40,000',
               '$40,000-$50,000', '$50,000-$60,000', '$60,000-$70,000',
               '$70,000-$80,000', '$80,000-$100,000', '$100,000-$150,000',
               '$150,000-$250,000', '$250,000-$500,000', '$500,000-$1,000,000',
               'More than $1,000,000'],
    'religion': ['8', 'agnostic', 'atheist', 'christian', 'jewish', 'catholic',
                 'muslim', 'hindu', 'buddhist', 'other'],
    'monogamy': ['73', 'monogamous', 'non-monogamous'],
    'diet': ['54', 'vegetarian', 'vegan', 'kosher', 'halal'],
    'sign': ['21', 'acquarius', 'pisces', 'aries', 'taurus', 'gemini',
             'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius',
             'capricorn'],
    'ethnicity': ['9', 'asian', 'middle eastern', 'black', 'native american',
                  'indian', 'pacific islander', 'hispanic/latin', 'white',
                  'human (other)']
}


dogs = ['owns dogs', 'likes dogs', 'dislikes dogs']
cats = ['owns cats', 'likes cats', 'dislikes cats']


def get_height_query(height_min, height_max):
    '''Convert from inches to millimeters/10'''
    min_int = 0
    max_int = 99999
    if height_min is not None:
        min_int = int(height_min) * 254
    if height_max is not None:
        max_int = int(height_max) * 254
    return '10,{0},{1}'.format(str(min_int), str(max_int))


def get_options_query(type, inputs):
    for char in sep_replacements:
        inputs = [input.replace(char, '') for input in inputs]
    inputs = [input.lower() for input in inputs]
    if type in binary_lists:
        start = 1
        option_list = binary_lists[type]
    if type == 'drugs':
        start = 0
    if type == 'diet':
        start = 2
    int_to_return = 0
    for power, option in enumerate(option_list[1:], start=start):
        for char in sep_replacements:
            option = option.replace(char, '')
        if option in inputs:
            int_to_return += 2**power
    return '{0},{1}'.format(option_list[0], int_to_return)


def get_pet_queries(pets):
    for char in sep_replacements:
        pets = [pet.replace(char, '') for pet in pets]
    pets = [pet.lower() for pet in pets]
    dog_int = 0
    cat_int = 0
    for power, option in enumerate(dogs, start=1):
        for char in sep_replacements:
            option = option.replace(char, '')
        if option in pets:
            dog_int += 2**power
    for power, option in enumerate(cats, start=1):
        for char in sep_replacements:
            option = option.replace(char, '')
        if option in pets:
            cat_int += 2**power
    dog_query = '16,{0}'.format(dog_int)
    cat_query = '17,{0}'.format(cat_int)
    return dog_query, cat_query


def get_kids_query(kids):
    kids = [kid.lower() for kid in kids]
    kid_int = 0
    include_has = False
    include_wants = False
    for option in kids:
        if option in has_kids:
            include_has = True
        elif option in wants_kids:
            include_wants = True
    if include_has and not include_wants:
        for option in kids:
            if option in has_kids:
                kid_int += has_kids[option]['addition']
    elif include_wants and not include_has:
        for option in kids:
            if option in wants_kids:
                kid_int += wants_kids[option]['addition']
    elif include_wants and include_has:
        for has_option in kids:
            if has_option in has_kids:
                for wants_option in kids:
                    if wants_option in wants_kids:
                        kid_int += 2**(has_kids[has_option]['power'] + wants_kids[wants_option]['power'])
    return '18,{0}'.format(kid_int)


def get_language_query(language):
    return '22,{0}'.format(language_map[language.title()])


hour = 60*60
join_date_string_to_int = {
    'hour': hour,
    'day': hour*24,
    'week': hour*24*7,
    'month': hour*24*30,
    'year': 365*24*hour
}


def get_join_date_query(date):
    date_int = 0
    if isinstance(date, str) and not date.isdigit():
        if date in join_date_string_to_int:
            date_int = join_date_string_to_int[date]
        else:
            date_int = int(date)
    else:
        date_int = date
    return '6,{0}'.format(date_int)
