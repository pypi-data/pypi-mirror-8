#!/usr/bin/env python3

__all__ = ["get_info", "strip_site", "InfoExtractor"]

import re

from ..utils import (strip_site, std, MGet, urlparse, ExtractorError)
from ..utils import common as _common
from .common import InfoExtractor
from .anivids import Anivids_IE
from .aniupload import Aniupload_IE
from .auengine import Auengine_IE
from .ftwcdn import Ftwcdn_IE
from .mp4upload import Mp4upload_IE
from .playpanda import Playpanda_IE
from .play44 import Play44_IE
from .trollvid import Trollvid_IE
from .veevr import Veevr_IE
from .videonest import Videonest_IE
from .videodrive import Videodrive_IE
from .yourupload import Yourupload_IE

_ALL_CLASSES = [klass for name, klass in globals().items() if name.endswith('_IE')]
MANGA_URL = r'^(?:https?://)?(?:www\.)?mangafox\.me/manga/(.+?)/v([0-9]+)/c([0-9]+)/([0-9]+\.html)'
EG_url = "http://mangafox.me/manga/v${01}/c${001}/${1}.html"

def get_info_extractor(ie_name):
	return globals()[ie_name.capitalize()+'_IE']

def get_info(url, client, info):
	newurl = None; result = {}
	hostname, site = strip_site(url)
	ret = {	'url': url,
		'site': site,
		'hostname': hostname,
		'filename': InfoExtractor.getFilename(url)}

	wpage = info.get('wpage')

	MGet().init_(	site	= site,
			wpage	= wpage,
			cdl	= info.get('cur_download',1),
			tot	= info.get('tot_download',1) if not info.get('down-mange') else "",
			epage	= info.get('embedurl'))

	if info.get('mirror'): return ret

	if info.get('down-mange'):
		if re.match(MANGA_URL, url):
			mObj = re.search(MANGA_URL, url)
			match = mObj.groups()
		else: common.report_error("Mangafox url must match " + eg_url)

		try: re_data = InfoExtractor().gen_manga_urls (url,client=client, \
							wpage=wpage,spage=info.get("manga-page"))
		except:	raise ExtractorError("unable to find manga information from: %s" % hostname)

		ret["urls"] = re_data["urls"]
		ret["series"] = re_data["series"]
		ret["chapter"] = re_data["chapter"]
		ret["tot_download"] = re_data["tot_download"]
		return ret

	if hostname in ('animeram.eu','animeram.tv','animewaffles.tv','cc-anime.com'):
		try: newurl = InfoExtractor.get_embed_url(url,client=client,wpage=wpage)
		except: raise ExtractorError("unable to find embed url in: %s" % hostname)

	if newurl is not None:
		hostname, site = strip_site(newurl)
		if not info.get('embedurl'): _common.report("Embed url: %s" % newurl)
		ret['url'] = newurl
		ret['hostname'] = hostname

	if info.get('embedurl'): return ret

	hostname, site = strip_site(ret.get('url'))
#	format = info.get('v_format', 18)

	if hostname in std.site_list:
		try:
			ie = get_info_extractor(site)
			res= ie(ret.get('url'),
				client 	= client,
				wpage	= wpage,
				format	= 18 )

		except: raise ExtractorError("Unable to Extract: %s " % (hostname))
		result = res._extract_info()
	else: return ret

	if result is None: raise ExtractorError ("Unable to Extract: %s " % (hostname))
	result['hostname'] = ret.get('hostname')

	return result

