from django.shortcuts import render, get_object_or_404, redirect
from .models import Linker,flexibility
from django.http import HttpResponseRedirect
import sys  
from django.views.generic import ListView
from django.db.models import Q # new
from django.shortcuts import render
import ast
import pandas as pd
import plotly.express as px
from plotly.offline import plot
from .forms import LinkerForm


# render the search_results.html template
def search_view(request):
    return render(request, 'search_results.html')


# querying the dataset
class SearchResultsView(ListView):
    model = Linker
    template_name = 'search_results.html'

    def get_queryset(self):
        query = str(self.request.GET.get('query'))  # get the 'query' input from the form and convert it to a string
        print("Query:", query)  # print the value of query (command line)
        if query:
            object_list = Linker.objects.filter(
                Q(id__icontains=query)
            )
        else:
            object_list = Linker.objects.none()  # return an empty queryset if no query is provided
        return object_list
    

#return the linker's information and flexibility graph
def graph_data(request,idurl):
    #search through linker database and extract information related to the linker
    linker = get_object_or_404(Linker, id=idurl)
    
    #if the length of linker is greater or equal to 5
    #perform the following function to output the flexibility graph
    if linker.length >=5:
        data_instance = flexibility.objects.get(id=idurl)
        sequence_list=data_instance.Sequence
        char_list_str = data_instance.backbone  
        #conver the list of strings to numbers
        char_list = ast.literal_eval(char_list_str)    

        #index amino acid
        index_list=[]
        for i in range(1,len(sequence_list)+1):
            index=sequence_list[i-1]+str(i)
            index_list.append(index)

        #combined the index list and backbone dynanmic into one dataframe 
        df=pd.DataFrame(list(zip(index_list,char_list)),columns=['residue index','S^2'])
        df = df.reset_index(drop=True)

        #plot
        fig=px.line(df, x='residue index', y="S^2")

        fig.update_layout(title='Backbone Dynamic',yaxis_range=[df['S^2'][0]-0.2,1])

        
        fig.add_shape(type="rect",
                x0=df['residue index'][0], y0=0.69,
                x1=df['residue index'][len(df)-1], y1=0.8,
                fillcolor='rgba(0, 255, 0, 0.3)',
                line=dict(color='rgba(0, 0, 0, 0)'))

        # Add the annotation outside the graph
        fig.add_annotation(
            xref='paper', x=0,  # Position the annotation outside the left side of the graph
            yref='paper', y=1,  # Position the annotation at the top of the graph
            text="Rigid",  # Text of the annotation
            showarrow=False,  # Hide the arrow
            font=dict(color='black', size=15)  # Font style
        )

        # Add the annotation outside the graph
        fig.add_annotation(
            xref='paper', x=0,  # Position the annotation outside the left side of the graph
            yref='paper', y=0,  # Position the annotation at the top of the graph
            text="Flexible",  # Text of the annotation
            showarrow=False,  # Hide the arrow
            font=dict(color='black', size=15)  # Font style
        )

        # Add the annotation outside the graph
        fig.add_annotation(
            x=index_list[1],  # Position the annotation outside the left side of the graph
            y=0.75,  # Position the annotation at the top of the graph
            text="Context Dependent",  # Text of the annotation
            showarrow=False,  # Hide the arrow
            font=dict(color='black', size=15)  # Font style
        )

        #pass to the template
        dynamic_plot=plot(fig, output_type="div")
        context={
            'plot_dyna':dynamic_plot,
            'linker': linker
            
            }
        return render(request,'linker_details.html', context)
    else:
        return render(request, 'linker_details.html', {'linker': linker})
                
def multiselect(request):
    if request.method=='POST':
        length_selection=request.POST.getlist('lengths')
        flexibility_selection=request.POST.getlist('Flexibility')
    else:
        length_selection=[]
        flexibility_selection=[]
    
    length_selected_items=Linker.objects.none()
    for i in length_selection:
        if i=='Short':
            length_selected_items=length_selected_items|Linker.objects.filter(length__lte=5)
        if i=='Medium':
            length_selected_items=length_selected_items|Linker.objects.filter(length__range=(6,12))
        if i=='Long':
            length_selected_items=length_selected_items|Linker.objects.filter(length__gte=12)

    idlist=[]
    for items in length_selected_items:
        idlist.append(items.id)

    flex_selected_items=flexibility.objects.none()
    for id in idlist:
        flex_selected_items=flex_selected_items|flexibility.objects.filter(id__iexact=id)

    queryset2=flexibility.objects.none()
    for i in flexibility_selection:
        if i=='Flexible':
            queryset2=queryset2|flex_selected_items.filter(average_flexibility__lt=0.69)
            
        if i=='Intermediate':
            queryset2=queryset2|flex_selected_items.filter(average_flexibility__range=(0.69,0.81))
        if i=='Rigid':
            queryset2=queryset2|flex_selected_items.filter(average_flexibility__gt=0.81)
        
    context = {
        'selected_items': queryset2
    }

    return render(request,'results.html',context)


def add_linker(request):
    submitted=False
    '''
    if request.method=="POST":
        form=LinkerForm(request.POST) #fill out the form and they are posted
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('?submitted=True') #sending it to the get request
            #return HttpResponseRedirect(reverse('add_venue') + '?submitted=True')
        
    else:
        form=LinkerForm
        if "submitted" in request.GET:
            submitted=True

    return render(request,'linkerform.html',{'form':form,'submitted':submitted})
   '''