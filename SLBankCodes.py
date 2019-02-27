
# coding: utf-8

# In[165]:


#http://www.thebankcodes.com/srilanka_banks/results.php?searchstring=Sampath+Bank+PLC&page=1


# In[171]:


def log_progress(sequence, every=None, size=None, name='Items'):
    from ipywidgets import IntProgress, HTML, VBox
    from IPython.display import display

    is_iterator = False
    if size is None:
        try:
            size = len(sequence)
        except TypeError:
            is_iterator = True
    if size is not None:
        if every is None:
            if size <= 200:
                every = 1
            else:
                every = int(size / 200)     # every 0.5%
    else:
        assert every is not None, 'sequence is iterator, set every'

    if is_iterator:
        progress = IntProgress(min=0, max=1, value=1)
        progress.bar_style = 'info'
    else:
        progress = IntProgress(min=0, max=size, value=0)
    label = HTML()
    box = VBox(children=[label, progress])
    display(box)

    index = 0
    try:
        for index, record in enumerate(sequence, 1):
            if index == 1 or index % every == 0:
                if is_iterator:
                    label.value = '{name}: {index} / ?'.format(
                        name=name,
                        index=index
                    )
                else:
                    progress.value = index
                    label.value = u'{name}: {index} / {size}'.format(
                        name=name,
                        index=index,
                        size=size
                    )
            yield record
    except:
        progress.bar_style = 'danger'
        raise
    else:
        progress.bar_style = 'success'
        progress.value = index
        label.value = "{name}: {index}".format(
            name=name,
            index=str(index or '?')
        )


# In[172]:


from requests import session
from itertools import cycle
import json
from bs4 import BeautifulSoup
import pandas as pd
import re


# In[176]:


import random
user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


# In[177]:


import requests
from lxml.html import fromstring
def get_proxies():
    user_agent = random.choice(user_agent_list)
    #Set the headers 
    headers = {'User-Agent': user_agent}
    url = 'https://free-proxy-list.net/'
    response = requests.get(url, headers=headers)
    #print(response.text)
    parser = fromstring(response.text)
    proxies = set()
    #print(parser.xpath('//tbody/tr'))
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


# In[179]:


banks = [
    {'bank_name':'Sampath_Bank_PLC'
     , 'total_pages':15
     , 'start_page': 1
    }
    , 
    {'bank_name':'Commercial_Bank_PLC'
     ,'total_pages':17
     , 'start_page':1
    }
    , 
    {'bank_name':'Bank_of_Ceylon'
       ,'total_pages':38
       , 'start_page':1
      }
    , 
    {'bank_name':'Hatton_National_Bank_PLC'
       ,'total_pages':15
       , 'start_page':1
      }
    , 
    {'bank_name':'National_Development_Bank_PLC'
       ,'total_pages':6
       , 'start_page':1
      }
    , 
    {'bank_name':'Nations_Trust_Bank_PLC'
       ,'total_pages':6
       , 'start_page':1
      }
    , 
    {'bank_name':'Peoples_Bank'
       ,'total_pages':24
       , 'start_page':1
      }
    , 
    {'bank_name':'Seylan_Bank_PLC'
       ,'total_pages':9
       , 'start_page':1
      }
    , 
    {'bank_name':'Regional_Development_Bank'
       ,'total_pages':19
       , 'start_page':1
      }
    , 
    {'bank_name':'Cargills_Bank_Limited'
       ,'total_pages':1
       , 'start_page':1
      }
    , 
    {'bank_name':'National_Savings_Bank'
       ,'total_pages':16
       , 'start_page':1
      }
    ]


# In[180]:


def call_request(start_page,total_pages,bank_search_code, elapsed):
    for i in log_progress(range(start_page,total_pages+1), every=1, name=bank_search_code):
        #Pick a random user agent
        user_agent = random.choice(user_agent_list)
        #Set the headers 
        headers = {'User-Agent': user_agent}
        proxy = next(proxy_pool)

        url = 'http://www.thebankcodes.com/srilanka_banks/bank_results.php?searchstring='+bank_search_code+'&page='+str(i)
        try:
            page_response = c.get(url, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=5)
            if page_response.status_code != 200:
                raise Exception
                # notify, try again
        except:
            start_page = elapsed + 1
            call_request(start_page,total_pages,bank_search_code, elapsed)
            break
        elapsed = elapsed + 1
        soup = BeautifulSoup(page_response.content, "html.parser")

        table = soup.find('table', {"id": "resptable"}).find('tbody')

        for tr in table.findAll('tr'):
            td = tr.findAll('td')
            bank_name = td[0].find('b').text

            branch_code = td[1].text.split(' ')[2][4:]
            branch_name = td[2].text.split('Name:')[1][1:]

            if len(branch_code)==1:
                branch_code = "00" + branch_code
            elif len(branch_code)==2:
                branch_code = "0" + branch_code

            branch_codes.append(branch_code)
            branch_names.append(branch_name)
            bank_names.append(bank_name)


# In[181]:


branch_codes = []
branch_names = []
bank_names = []

with session() as c:
    for bank in log_progress(banks, name='all banks'):
        bank_search_code = bank['bank_name']
        total_pages = bank['total_pages']
        start_page = bank['start_page']

        proxies = get_proxies()
        print(proxies)
        proxy_pool = cycle(proxies)
        
        elapsed = 0
        
        call_request(start_page, total_pages, bank_search_code, elapsed)
        
    df=pd.DataFrame(branch_codes,columns=['branch_code'])
    df['branch_name'] = branch_names
    df['bank'] = bank_names
    df.to_csv('bank_codes.csv')
    dfs.append(df)
    




    
    

