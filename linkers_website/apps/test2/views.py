
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import testdata
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import sys
import json
import pandas as pd
from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
import ast
import pandas as pd



def searchdata(request):
    if request.method=="POST":
        searched=request.POST['searched']
        #query=request.GET.get('searched')
        data=testdata.objects.filter(id__contains=searched)

        return render(request, 'searchresults.html', {'searched':searched,'data':data})
    else:
         return render(request, 'test2.html', {})


        
#, id="1qhaA_1"
def graph_data(request,id):

    #query=request.GET.get('q','')
    #search_results=testdata.objects.filter(name__icontains=query)
    
   
    # Query the specific data based on the ID string
    data_instance = testdata.objects.get(id=id)
    sequence_list=data_instance.Sequence
    char_list_str = data_instance.backbone  # Assuming the values are separated by commas
    char_list = ast.literal_eval(char_list_str)

    # Convert char list to numbers
    numbers_list = [float(value) for value in char_list]

    # Create a Plotly graph
        

    index_list=[]
    for i in range(1,len(sequence_list)):
        index=sequence_list[i-1]+str(i)
        index_list.append(index)

    df=pd.DataFrame(list(zip(index_list,char_list)),columns=['residue index','S^2'])
    df = df.reset_index(drop=True)

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
        'plot_dyna':dynamic_plot
        
        }
    return render(request,'graph.html', context)