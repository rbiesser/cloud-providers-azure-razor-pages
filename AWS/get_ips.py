#!/usr/bin/env python
import requests
import json

# https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html#filter-json-file

# The original example script called for getting all amazon ips, but we only care about unique
# regions since all the ips in the region are given the same geographical locations.

# https://ipstack.com/ access key (free)
access_key = '<access_key>'

# only need the items in the prefixes array
ip_ranges = requests.get('https://ip-ranges.amazonaws.com/ip-ranges.json').json()['prefixes']

unique_regions = ['GLOBAL']
amazon_ips_regions = []
     
for ip in ip_ranges:
    if ip['region'] not in unique_regions:
        unique_regions.append(ip['region'])

        geoip = requests.get('http://api.ipstack.com/'+ip['ip_prefix'].split('/')[0]+'?access_key='+access_key).json()
        # print(json.dumps(geoip, indent=2))

        ip['name'] = ip['region']
        # this would be easier if Amazon would give us a display name
        # displayName = ip['region'].split('-')
        # displayName[0] = displayName[0].upper()
        # displayName[1] = displayName[1].title()
        # ip['displayName'] = ' '.join(displayName)
        ip['displayName'] = ip['name'].replace('-', ' ').title()
        ip['latitude'] = str(geoip['latitude'])
        ip['longitude'] = str(geoip['longitude'])
        del ip['region']
        amazon_ips_regions.append(ip)

print(json.dumps(amazon_ips_regions, indent=2))