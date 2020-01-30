#!/usr/bin/env python
import requests
import json
import time

# ATTENTION: script is incomplete as-is but was used to create gcp-regions.json

# I searched for hours and couldn't find a suitable geoip database that gave reliable results so,
# this list ended up being a manual process checking multiple sites looking for unique locations.
# They sort of match up to this list: https://cloud.google.com/compute/docs/regions-zones
# Again the ip doesn't matter since this project is just identifying locations.

# https://ipstack.com/ - free key
# https://ipapi.co/ - sometimes displays add instead of real data on free version and rate limits, but no signup
# https://ipgeolocation.io/ - free key
# https://ipinsight.io/ - free key; seems to be the most up to date although missing some found in others


# https://cloud.google.com/compute/docs/faq#networking
# https://www.reddit.com/r/starcitizen/comments/3lce2k/list_of_google_cloud_ip_addresses_for_firewall/
# https://gist.github.com/n0531m/f3714f6ad6ef738a3b0a
# dig @8.8.8.8 +short txt _cloud-netblocks.googleusercontent.com | \
#     sed 's/"//g; s/ip4://g; s/ip6://g;' | tr ' ' '\n' | grep include | cut -d ':' -f2 | xargs \
#     dig @8.8.8.8 +short txt | sed 's/"//g; s/ip4://g; s/ip6://g;' | tr ' ' '\n' | grep '/'

# dig @8.8.8.8 +short txt _cloud-netblocks.googleusercontent.com
# "v=spf1 
#     include:_cloud-netblocks1.googleusercontent.com 
#     include:_cloud-netblocks2.googleusercontent.com 
#     include:_cloud-netblocks3.googleusercontent.com 
#     include:_cloud-netblocks4.googleusercontent.com 
#     include:_cloud-netblocks5.googleusercontent.com 
#     ?all"

# https://ipstack.com/ access key (free)
# access_key = 'apikey'

# https://app.ipgeolocation.io/ (free)
access_key = 'apikey'

# ipapi will give RateLimited error if you don't set user-agent
session = requests.Session()
session.headers.update({'User-Agent': 'Free Plan'})

# loc = session.get('https://ipapi.co/8.8.8.8/json/')
# print loc.json()

ip = dict()
unique_regions = []
gcp_ips_regions = []

with open('ip-ranges.txt', 'r') as f:
    for line in f:
        ip['network'] = line.split('/')[0]

        # print(ip['network'])
        # geoip = requests.get('http://api.ipstack.com/'+ip['network']+'?access_key='+access_key).json()
        # geoip = session.get('https://ipapi.co/'+ip['network']+'/json/').json()
        geoip = session.get('https://api.ipgeolocation.io/ipgeo?apiKey='+access_key+'&ip='+ip['network']).json()
        # print(json.dumps(geoip, indent=2))
        # break

        # if geoip['zipcode'] not in unique_regions:
        #     unique_regions.append(geoip['zipcode'])
        ip['name'] = geoip['city']
        ip['displayName'] = geoip['country_name']
        ip['latitude'] = str(geoip['latitude'])
        ip['longitude'] = str(geoip['longitude'])
        gcp_ips_regions.append(ip)

        print(json.dumps(ip, indent=2))

            # time.sleep(5)

# print(json.dumps(gcp_ips_regions, indent=2))