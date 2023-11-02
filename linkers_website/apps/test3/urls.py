from django.urls import path
from .views import  search_view, SearchResultsView,graph_data, multiselect,add_linker
app_name = "test3"

urlpatterns = [
    path('search/', search_view, name='search_results'),  # Function-based view
    path('multisearch/', multiselect, name='search'),  # Function-based view
    path('search/results/', SearchResultsView.as_view(), name='search_results_list'),  # Class-based view
    path('<str:idurl>/', graph_data, name='linker_sequence'), #Function-based view 
    path('add_linker',add_linker,name="addlinker")
    
    #path('',Multiplesearchtemp),
    
 

]