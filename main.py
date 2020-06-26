from google import google
import requests
from bs4 import * 
from urllib.parse import urlparse
from urllib.parse import urljoin
import urllib.parse

num_page = 6
Search_list = ["Managed Service Provider London", "It services London","IT support", "Junior Python needed", "Software services London" ]

exclude = []

def get_data(link):
    try:
        data = requests.get(link)
        return data.content
    except:
        return False


def search_links(data,term):


    output = []
    parsed = BeautifulSoup(data, 'html.parser')
    tags = parsed('a')
    for tag in tags:
        try:
            if term.lower() in tag.get('href',None):
                output.append(tag.get('href'))
        except:
            pass
    if output == []:
        return False
    else:
        return output
        
        
def check_valid(url,dir):
    if url in dir:
        return dir
    else:
        return urljoin(url,dir)
        
def url_to_base(link):
    buffer = urllib.parse.urlparse(link)
    result = '{uri.scheme}://{uri.netloc}/'.format(uri=buffer)
    return result
    
def url_to_domain(link):
    buffer = urllib.parse.urlparse(link)
    return buffer.netloc
    

def convert_all(url):
    url = url_to_base(url)
    buffer = get_data(url)
    return buffer

for query in Search_list:
    result = google.search(query, num_page)
    for links in result:
        base = url_to_base(links.link)
        domain = url_to_domain(links.link)
        if not any(domain in s for s in exclude):
            
            data = convert_all(links.link)
        else:
            #print("Skipping! ", domain)
            continue
        
        if data:
        
            search_result = search_links(data,"career")
            email_string = "@" + domain
            email_harvest = search_links(data,email_string)
            
            if search_result:
                
                for final_result in search_result:
                    if any(domain in s for s in exclude):
                        #print("Already discovered! ,",domain)
                        break
                    else:
                    
                        full_url = check_valid(base,final_result)
                        
                        exclude.append(domain)
            if email_harvest:
                for emails in email_harvest:
                    print(full_url, "Email: ", emails)
        




                
    

