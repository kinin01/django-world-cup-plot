from typing import List
from django.utils import timezone
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests

from core.models import Fixture


class Command(BaseCommand):
    help = 'Load data'

    def handle(self, *args, **kwargs):
        urls = self.construct_urls()
        for url in urls:
            response = requests.get(url)

            soup = BeautifulSoup(response.content, 'html.parser')
           
            results = soup.find_all('div', class_='sp-c-fixture_wrapper')
            
            for result in results:
                home = result.select_one('.sp-c-fixture_team-name--home .qa-full-team-name').txt
                away = result.select_one('.sp-c-fixture_team-name--away .qa-full-team-name').txt
                home_goals = result.select_one('.sp-c-fixture_number--home').txt
                away_goals = result.select_one('.sp-c-fixture_number--away').txt
                Fixture.objects.get_or_create(
                    team1=home,
                    team2=away,
                    team1_goals=home_goals,
                    team2_goals=away_goals
                )
        
    def construct_urls(self): 
        BASE_URL = "https://www.bbc.co.uk/sport/football/world-cup/scores-fixtures/"
        START_DATE = timezone.datetime(year=2022, month=11, day=20)
        END_DATE = timezone.datetime(year=2022, month=12, day=18)
        delta = (END_DATE-START_DATE).days
        
        urls = []
        for i in range(delta+1):
            date = START_DATE + timezone.timedelta(days=i)
            date = date.strftime("%y-%m-%d")
            urls.append(f"{BASE_URL}{date}")
            
        return urls
            