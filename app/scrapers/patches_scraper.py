from lxml import html
from app.models import Patch
import requests
from operator import itemgetter
from django.core.exceptions import ObjectDoesNotExist

class PatchesCollector:
    @staticmethod
    def scrape():
        page = requests.get('http://dota2.gamepedia.com/Game_Versions')
        tree = html.fromstring(page.content)

        patches = []

        versions = tree.xpath('//table[@class="wikitable"][1]/tr/td[1]//text()[2]')

        for i, version in enumerate(versions):
            date = tree.xpath('//table[@class="wikitable"][1]/tr[{}]/td[3]//text()[2]'.format(i+3))
            if len(date) != 0:
                patches.append({"version": version, "date": date[0]})
        return patches

    @staticmethod
    def is_patch_recorded(version):
        try:
            return Patch.objects.get(pk=version) != None;
        except ObjectDoesNotExist as e:
            return False

    @staticmethod
    def sync_patches():
        patches_scraped = PatchesCollector.scrape()
        patches_scraped.sort(key=itemgetter('date'))
        new_patches = []
        for patch in patches_scraped:
            if not PatchesCollector.is_patch_recorded(patch['version']):
                patch = Patch(version=patch['version'], start_date=patch['date'])
                patch.save()
                new_patches.append(patch)
        return new_patches
