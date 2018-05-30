import aylien_news_api
from aylien_news_api.rest import ApiException
import re
import pdb

def ay_lookup(keyword, entities = [], timeframe = '0,2', league=''):
    # Configure API key authorization: app_id
    aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = '115c381f'
    # Configure API key authorization: app_key
    aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = '876fb6a2163fec8db0b725304363eb78'

    # create an instance of the API class
    api_instance = aylien_news_api.DefaultApi()

    codes = {}
    codes['NFL'] = ['15003000']
    codes['MLB'] = ['15007000']
    codes['NBA'] = ['15008000']
    codes['NHL'] = ['15031000']
    codes[''] = []

    categories = ['15000000','15073000']

    categories += codes[league]

    opts = {
      'title': keyword,
      'body': keyword,
      'sort_by': 'relevance',
      'language': ['en'],
      'entities_body_text' : entities,
      'categories_taxonomy' : 'iptc-subjectcode',
      'categories_id' : categories
    }
    first = timeframe.split(',')[0]
    second = timeframe.split(',')[1]
    if first == '0':
        first = 'NOW'
    else:
        first = 'NOW-'+first+'DAYS'
    second = 'NOW-'+second+'DAYS'
    opts['published_at_start'] = second
    opts['published_at_end'] = first
    counter = 0
    try:
        api_response = api_instance.list_stories(**opts)
        for i in range(0, len(api_response.stories)):
            if counter < 10:
                counter += 1
                story = api_response.stories[i]
                if "Sign up for" not in story.body and "newsletter" not in story.body:
                    try:
                        body_clauses = clean_st(story.body).split('.')
                        while '' in body_clauses:
                            body_clauses.remove('')
                        body_clauses = fix_clauses(body_clauses)
                    except:
                        body_clauses = []
                    try:
                        summary = story.summary['sentences']
                    except:
                        summary = []
                    summarycounter = 0
                    bodycounter = 0
                    st = ''
                    while '' in body_clauses:
                        body_clauses.remove('')
                    while bodycounter < len(body_clauses) and st == '':
                        try:
                            st = summary[summarycounter]
                            initial = summarycounter
                            summarycounter += 1
                            lst = body_clauses
                        except:
                            st = body_clauses[bodycounter]+"."
                            initial = bodycounter
                            bodycounter += 1
                            lst = summary
                        top = initial + 1
                        st = clean_st(st)
                        while bad_string(st) and top < len(lst):
                            if lst[initial:top] != []:
                                st = lst[initial:top].join('.') + '.'
                            top += 1
                        if 'photo' in st.lower() or 'file' in st.lower() or st[0] == st[0].lower() or '(' in st or ')' in st:
                            st = ''
                        st = clean_st(st)
                    if len(st) > 10 and bad_string(st) != True:
                        return story, st
                else:
                    return {}, ''
    except ApiException as e:
        print("Exception when calling DefaultApi->list_stories: %s\n" % e)

def bad_string(st):
    try:
        if regex_check(clean_st(st)) == False:
            return True
        elif len(st) < 15:
            return True
        else:
            return False
    except:
        return True

def regex_check(st):
    if st[-1] == '.':
        st = st[:-1]
    t = ' '+st
    if re.match("(?! .)", t[len(t)-2:]) == None:
        return False
    if re.match("(?! ..)", t[len(t)-3:]) == None:
        return False
    if re.match("(?! ...)", t[len(t)-4:]) == None:
        return False
    return True


def clean_st(st):
    if st == '':
        return st
    try:
        if 'About ' in st[:6]:
            st = st[6:]
    except:
        pass
    st = st.replace('\n',' ')
    while st != '' and st[0] == ' ':
        st = st[1:]
    while st != '' and st[-1] == ' ':
        st = st[:len(st)-1]
    while '  ' in st:
        st = st.replace('  ',' ')
    while '..' in st:
        st = st.replace('..','.')
    while ' .' in st:
        st = st.replace(' .','')
    return st

def fix_clauses(clauses):
    if len(clauses) < 2:
        return clauses
    else:
        current = 0
        extra = current + 1
        clauses[0] = clean_st(clauses[0])
        while extra < len(clauses):
            if len(clauses[current]) < 20 or len(clauses[extra]) < 20 or bad_string(clauses[current]):
                clauses[current] = clauses[current] + '. ' + clean_st(clauses[extra])
                clauses.remove(clauses[extra])
            else:
                current += 1
                extra = current + 1
        return clauses
