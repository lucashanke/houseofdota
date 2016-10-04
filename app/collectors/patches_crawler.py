from lxml import html
from app.models import Patch
import requests
from operator import itemgetter
from django.core.exceptions import ObjectDoesNotExist
from bs4 import BeautifulSoup

class PatchesCrawler:
    @staticmethod
    def _crawl():
        page = requests.get('http://dota2.gamepedia.com/Game_Versions')
        soup = BeautifulSoup(page.content, 'html.parser')

        patches = []
        table = soup.find_all('table', class_="wikitable")[0]

        for line in table.find_all('tr'):
            columns = line.find_all('td')
            if len(columns) > 3:
                version = columns[0].get_text().rstrip().strip()
                date = columns[2].get_text().rstrip().strip()
                if date is not '-':
                    patches.append({"version": version, "date": date})
        return patches

    @staticmethod
    def is_patch_recorded(version):
        try:
            return Patch.objects.get(pk=version) != None;
        except ObjectDoesNotExist as e:
            return False

    @staticmethod
    def sync_patches():
        patches_scraped = PatchesCrawler._crawl()
        patches_scraped.sort(key=itemgetter('date'))
        new_patches = []
        for patch in patches_scraped:
            if not PatchesCrawler.is_patch_recorded(patch['version']):
                patch = Patch(version=patch['version'], start_date=patch['date'])
                patch.save()
                new_patches.append(patch)
        return new_patches
