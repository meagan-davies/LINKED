from django.urls import path
from .views import graph_data, searchdata

app_name = "test2"

urlpatterns = [
    path('',searchdata,name='search'),
    path('graph/<str:id>/',graph_data,name='graph')
    #path('search/results/', SearchResultsView.as_view(), name='search_results')
    #path('search/', graph_data, name='results'),
]
