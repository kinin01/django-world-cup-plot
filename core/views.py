from django.db.models import Q 
from django.shortcuts import render
from core.models import Fixture
import plotly.express as px

# Create your views here.
def scores(request):
    fixtures = Fixture.objects.all()
    teams = fixtures.values_list('team1',flat=true).distinct()
    goals = {}
    for team in teams:
        team_fixtures = fixtures.filter(Q(team1=team) | Q(team2=team))
        total_goals = sum([fix.get_goals(team) for fix in team_fixtures])
        goals[team] = total_goals
        
        fig = px.bar(x=goals.keys(), y=goals.values(), title=wc 2022, heaight=800)
        context = {'chart' : fig.to_html()}
    
    return render(request, 'index.html', context)