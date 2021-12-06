import pandas as pd
import numpy as np
import re
from tqdm import tqdm

import requests
from bs4 import BeautifulSoup
import pickle

# base_url = 'https://ecode360.com'
class TreeSpider():
    def __init__(self, base_href, base_url = 'https://ecode360.com'):
        self.base_href = base_href
        self.base_url = base_url
        self.all_href_lst = []
        self.tables = {}
        self.error_signals = []
        
    # archived
    def find_root(self):
        print('[DEBUG] Finding at:', self.base_href)
        soup = self.get_soup(self.base_href)
        potential_roots = []
        for link in (soup.find_all('a')):
            if 'land development' in link.text.lower():
                potential_roots.append(link.attrs['href'])
        #if len(np.unique(potential_roots)) > 1:
        #    print('[ERROR] More than one zoning page found!')
        #    return -1
        root_href = potential_roots[0]
        return root_href
    
    def get_soup(self, href):
        #print(self.base_url + href)
        res = requests.get(self.base_url + href)
        soup = BeautifulSoup(res.text, features="lxml")
        return soup

    def clean_text(self, text):
        text = re.sub('\n+', '\t', text)
        text = re.sub('\t+', '\t', text)
        text = text.strip()
        return text

    def get_page(self, href, parent):
        if href in self.all_href_lst:
            return -1
        if parent.height == 5:
            return -1
        #print('[DEBUG] curr href:', href)
        curr_node = ContentTreeNode(href, parent.height + 1)
        curr_node.parent = parent
        parent.children.append(curr_node)
        self.all_href_lst.append(href)
        
        soup = self.get_soup(href)
        if curr_node.href == self.base_href:
            curr_node.title = 'root'
        else:
            curr_node.title = self.clean_text(soup.find_all(attrs = {'id': 'pageTitle'})[0].text)
        child_contents = soup.find_all(attrs = {'id': 'childContent'})
        curr_node.sub_page_lst = self.get_sub_page_lst(soup)
        #print('[DEBUG] curr child_contents length:', len(child_contents))
        if len(child_contents) == 0:
            #print(curr_node.sub_page_lst)
            curr_node.is_leaf = False
            for child_href in curr_node.sub_page_lst:
                #curr_node.children.append(self.get_page(child_href, curr_node))
                self.get_page(child_href, curr_node)
                #print(curr_node.children)
        else:
            curr_node.is_leaf = True
            for href in curr_node.sub_page_lst:
                self.all_href_lst.append(href)
            content_str, table_lst = self.parse_leaf_page(child_contents[0])
            #curr_node.text_content = self.clean_text(content_str)
            curr_node.text_content = content_str
            curr_node.table_lst = table_lst
            self.tables[curr_node.title] = []
            for t in table_lst:
                self.tables[curr_node.title].append((t, curr_node.href))
            all_content, error_signal = leaf_node_processing(soup)
            curr_node.content = all_content
            self.error_signals.append(error_signal)
        return curr_node

    def get_sub_page_lst(self, soup):
        if len(soup.find_all(attrs = {'id': 'toc'})) == 0:
            return []
        children = soup.find_all(attrs = {'id': 'toc'})[0].find_all('a')
        children_href = [i['href'].replace('#', '/') for i in children]
        return list(np.unique(children_href))
    
    def parse_leaf_page(self, child_content):
        content_str = '\n[[START-PAGE]]\n'
        table_lst = []
        for child in child_content.children:
            #print('-=-=-=-=-=-=-=-=-=-=-=')
            try:
                child_classes = child.attrs['class']
            except:
                continue
            if 'sectionTitle' in child_classes:
                section_title = re.sub('\n+', ' ', child.text.strip())
                content_str += '\n'
                content_str += '[[SECTIONTITLE]]'
                content_str += '\n'
                content_str += section_title
                content_str += '\n'
            if 'content' in child_classes:
                content = re.sub('\n+', '\n', child.text.strip())
                content_str += '\n'
                content_str += '[[CONTENT]]'
                content_str += '\n'
                content_str += content
                content_str += '\n'
                content_str += '\n'
            child_tables = child.find_all('table')
            if len(child_tables) > 0:
                for table in child_tables:
                    try:
                        parsed_table = self.parse_table(table)
                    except:
                        continue
                    table_lst.append(parsed_table)
                    #self.table_lst.append(parsed_table)
        content_str += '\n[[END-PAGE]]\n'
        return content_str, table_lst

    def parse_table(self, table):
        all_rows = []
        for i in table.tbody.children:
            all_rows.append([c.text.strip() for c in i.children])
        return all_rows
    
    def run(self):
        # finding root
        #self.root_href = self.find_root()
        self.root_node = ContentTreeNode(self.base_href)
        self.root_node.root = True
        
        # scraping page
        self.get_page(self.base_href, self.root_node)
        self.root_node = self.root_node.children[0]
        self.root_node.parent = None
        #curr_node.parent = parent
        #parent.children.append(curr_node)
        
        # summary on errors
        all_errors = {}
        for err in self.error_signals:
            for k in err.keys():
                if k in all_errors.keys():
                    all_errors[k] += err[k]
                else:
                    all_errors[k] = err[k]
        self.error_signals = all_errors
    
    def print_tree(self, curr_node):
        prefix = curr_node.height * '  '
        print(prefix + '-=-=-=-=-=')
        print(prefix + curr_node.title)
        print(prefix + curr_node.text_content[:50])
        for child in curr_node.children:
            self.print_tree(child)
            
    def find_all_leaf_text(self):
        all_leaf_doc = []
        def find_leaf(node):
            if node.is_leaf:
                all_leaf_doc.append({
                    'title': re.sub('\t', ' ', node.title),
                    'text': node.text_content
                } )
            else:
                for child in node.children:
                    find_leaf(child)
        find_leaf(self.root_node)
        return all_leaf_doc
            
class ContentTreeNode():
    
    def __init__(self, href, height = 0):
        self.root = False
        self.height = height
        self.href = href
        self.sub_page_lst = []
        self.children = []
        self.text_content = ''
        self.title = ''
    
    def __repr__(self):
        repr_node = ''
        prefix = self.height * '  '
        repr_node += (prefix + '-=-=-=-=-=')
        repr_node += '\n'
        repr_node += (prefix + self.title)
        repr_node += '\n'
        repr_node += (prefix + self.text_content.replace('\n', '\n' + prefix))
        repr_node += '\n'
        for child in self.children:
            repr_node += child.__repr__()
        return repr_node

    
######## Experiment Zone ########
def clean_content(sent):
    import string
    printable_set = set(list(string.printable))
    sent = ''.join([c if c in printable_set else ' ' for c in sent])
    sent = re.sub('\n', ' ', sent)
    sent = re.sub(' +', ' ', sent)
    return sent

def leaf_node_processing(soup):
    error_signals = {
        'toc_list_empty': 0,
        'data_guid_not_found': 0,
        'content_lst_more_than_1': 0,
        'content_lst_not_found': 0
    }
    
    content_list = soup.find_all(attrs = {'id': 'toc'})
    if len(content_list) == 0:
        error_signals['toc_list_empty'] = 1
        return [], error_signals
    toc = content_list[0]
    href_list = toc.find_all('a')
    href_list = np.array([a['href'].replace('/', '').replace('#', '').strip() for a in href_list])
    href_list = np.unique(href_list)
    count_href = len(href_list)
    
    child_contents = soup.find_all(attrs = {'id': 'childContent'})[0]
    all_content = []
    for href in href_list:
        # title
        data_guid = ''
        data_guid_content = child_contents.find_all(attrs = {'data-guid': str(href)})
        for content in data_guid_content:
            data_guid += content.text.strip()
            data_guid += '\n'
        if data_guid == '':
            error_signals['data_guid_not_found'] += 1
        data_guid = clean_content(data_guid)
        
        # content
        content_lst = child_contents.find_all(attrs = {'id': str(href) + '_content'})
        #if len(content_lst) > 1:
        #    error_signals['content_lst_more_than_1'] += 1
        if len(content_lst) == 0:
            error_signals['content_lst_not_found'] += 1
        content_str = ''
        for i in range(len(content_lst)):
            content_str += clean_content(content_lst[i].text.strip())
            content_str += '\n'
        all_content.append({
            'href': href,
            'title': data_guid,
            'content': content_str
        })
    return all_content, error_signals