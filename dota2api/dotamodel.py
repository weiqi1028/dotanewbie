__author__ = 'wzhang'

# The module to build hero models

import urllib.request
import gzip
import re
import math
import json


def __get_skills(url):
    """get skiils list

    :param url: the hero url
    :returns: the skills list
    """
    
    string = __get_html(url)
    pattern = re.compile('skill-description\">\n<h3>(.*)</h3>')
    skill_list = pattern.findall(string)
    return skill_list


def __get_all_hero_urls():
    """get all the heroes relative urls

    :returns: the heroes relative urls list
    """
    
    hero_page = 'http://www.dotafire.com/dota-2/heroes'
    string = __get_html(hero_page)
    pattern = re.compile('<a href=\"(.*)\" class=\"hero-box')
    hero_url_list = pattern.findall(string)
    return hero_url_list


def __get_html(url):
    """send http request and returns the html documentation

    :param url: the url http request will send to
    :returns: the html doc
    """
    
    req = urllib.request.Request(url, headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept': 'text/html,application/xhtml+xml,'
        'application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-GB,en;q=0.8,en-US;q=0.6,zh-CN;q=0.4,zh;q=0.2,und;q=0.2'
        })

    opener = urllib.request.urlopen(req)
    data = opener.read()
    data = gzip.decompress(data)
    string = data.decode('utf-8')
    return string


def build_model():
    """build hero models, reference: http://www.dotafire.com

    :returns: a dictionary contains all the heroes similarities.
    Format:
    anti_mage: queen_of_pain: xxx, tinker: xxx...
    queen_of_pain: anti_mage: xxx, tinker: xxx...
    tinker: anti_mage: xxx, queen_of_pain: xxx...
    """
    
    base_url = 'http://www.dotafire.com'
    hero_urls = __get_all_hero_urls()
    except_heroes = ['arc_warden', 'pit_lord', 'oracle', 'techies']
    hero_names = []
    str_gain = []
    agi_gain = []
    int_gain = []
    primary_gain = []
    str_at_25 = []
    agi_at_25 = []
    int_at_25 = []
    health_at_25 = []
    mana_at_25 = []
    roles_array = []

    for hero_url in hero_urls:
        url = base_url + hero_url
        print('url: ' + url)
        start_index = hero_url.rfind('/')
        end_index = hero_url.rfind('-')
        hero_name = hero_url[start_index + 1: end_index]
        hero_name = hero_name.replace("-", "_")
        # print('hero name: ' + hero_name)
        
        if hero_name in except_heroes:
            continue

        hero_names.append(hero_name)
        
        html_doc = __get_html(url)
        pattern = re.compile('<div class=\"role-box\">(.*[\s\S]*?)</div>')
        role_box = pattern.findall(html_doc)
        
        # primary attribute
        pattern = re.compile('<td>Primary Attribute:</td><td> <span class=\"hilite[A-Z]\">(.*)</span>')
        primary_attribute = pattern.findall(role_box[0])[0]
        # print('Primary attribute: ' + str(primary_attribute))
        
        # attack type
        pattern = re.compile('<td>Attack Type:</td><td> <span class=\"hilite[A-Z]\">(.*)</span>')
        attack_type = pattern.findall(role_box[0])[0]
        # print('Attack type: ' + str(attack_type))
        
        # roles
        pattern = re.compile('<td>Role\(s\):</td><td> (.*)</td>')
        labels = pattern.findall(role_box[0])
        pattern = re.compile('<span class=\"hilite[A-Z]\">(.*?)</span>')
        roles = pattern.findall(labels[0])
        roles_array.append(roles)
        # print('roles: ' + str(roles))

        # stats
        pattern = re.compile('<span class=\"hilite[A-Z]\">(.*)</span> at 25')
        stats_at_25 = pattern.findall(html_doc)
        str25 = stats_at_25[0]
        agi25 = stats_at_25[1]
        int25 = stats_at_25[2]
        health25 = stats_at_25[3]
        mana25 = stats_at_25[4]
        
        str_at_25.append(str25)
        agi_at_25.append(agi25)
        int_at_25.append(int25)
        health_at_25.append(health25)
        mana_at_25.append(mana25)

        pattern = re.compile('\+ (.*)/level')
        attribute_per_level = pattern.findall(html_doc)
        str_per_level = attribute_per_level[0]
        agi_per_level = attribute_per_level[1]
        int_per_level = attribute_per_level[2]
        
        if primary_attribute == 'Strength':
            primary_gain.append(str_per_level)
        elif primary_attribute == 'Agility':
            primary_gain.append(agi_per_level)
        elif primary_attribute == 'Intelligence':
            primary_gain.append(int_per_level)

        str_gain.append(str_per_level)
        agi_gain.append(agi_per_level)
        int_gain.append(int_per_level)

    # debug information
    """
    print(hero_names)
    print(primary_gain)
    print(str_gain)
    print(agi_gain)
    print(int_gain)
    print(str_at_25)
    print(agi_at_25)
    print(int_at_25)
    print(health_at_25)
    print(mana_at_25)
    print(roles_array)
    """

    hero_num = len(hero_names)
    print('hero numbers: ' + str(hero_num))
    
    similarities = {}
    for i in range(hero_num):
        sim_dict = {}
        self_vector = [float(primary_gain[i]), float(str_gain[i]), float(agi_gain[i]), float(int_gain[i]), float(str_at_25[i])
                       , float(agi_at_25[i]), float(int_at_25[i]), float(health_at_25[i]), float(mana_at_25[i])]
        # hero i's roles
        self_roles = roles_array[i]

        for j in range(hero_num):
            if i == j:
                sim_dict[hero_names[j]] = 1
                continue
            target_vector = [float(primary_gain[j]), float(str_gain[j]), float(agi_gain[j]), float(int_gain[j]), float(str_at_25[j])
                             , float(agi_at_25[j]), float(int_at_25[j]), float(health_at_25[j]), float(mana_at_25[j])]
            # hero j's roles
            target_roles = roles_array[j]
            intersect = 0
            # calculate the intersection
            for self_label in self_roles:
                for target_label in target_roles:
                    if self_label == target_label:
                        intersect += 1

            # the score of two heroes' roles
            role_score = intersect / max(len(self_roles), len(target_roles))
            
            dot_product = 0
            mod1 = 0
            mod2 = 0
            for k in range(len(self_vector)):
                dot_product += self_vector[k] * target_vector[k]
                mod1 += math.pow(self_vector[k], 2)
                mod2 += math.pow(target_vector[k], 2)

            # the score based on heroe's attribute gain, health, mana, etc.
            value_score = dot_product / (math.sqrt(mod1) * math.sqrt(mod2))

            sim = 0.5 * role_score + 0.5 * value_score
            sim_dict[hero_names[j]] = sim
        similarities[hero_names[i]] = sim_dict

    # print(similarities['invoker'])
    # print(len(similarities['invoker']))
    with open('hero_similarities.json', 'w') as out_file:
        json.dump(similarities, out_file)
    out_file.close()