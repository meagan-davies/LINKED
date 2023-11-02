from django.shortcuts import render, get_object_or_404, redirect
from .models import Linker,flexibility,Hydrophobicity
from django.http import HttpResponseRedirect
import sys  
from django.views.generic import ListView
from django.db.models import Q # new
from django.shortcuts import render
import ast
import pandas as pd
import plotly.express as px
from plotly.offline import plot
from .forms import LinkerForm,FlexForm
import json,requests
import time

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import io
import base64
from PIL import Image
from io import BytesIO



# render the search_results.html template
def search_view(request):
    return render(request, 'search_results.html')


# querying the dataset
# this is for search box when user enters a string 
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

 
def lengthselect(length_selection):
    length_selected_items=Linker.objects.none()
    for i in length_selection:
        if i=='Short':     
            length_selected_items=length_selected_items|Linker.objects.filter(length__lte=5)
        if i=='Medium':
            length_selected_items=length_selected_items|Linker.objects.filter(length__range=(6,12))
        if i=='Long':
            length_selected_items=length_selected_items|Linker.objects.filter(length__gte=12)
 
    filtered_list=Linker.objects.none()
    for item in length_selected_items:
        filtered_list=filtered_list|Linker.objects.filter(id__iexact=item.id)

    return filtered_list

def flexselect(flexibility_selection):
    flex_selected_items=flexibility.objects.none()
    for i in flexibility_selection:
        if i=='Flexible':
            flex_selected_items=flex_selected_items|flexibility.objects.filter(type__iexact='flexible') 
        if i=='Intermediate':
            flex_selected_items=flex_selected_items|flexibility.objects.filter(type__iexact='context dependent (can be either flexible or rigid)')
        if i=='Rigid':
            flex_selected_items=flex_selected_items|flexibility.objects.filter(type__iexact='rigid')
    filtered_list=Linker.objects.none()
    for item in flex_selected_items:
        filtered_list=filtered_list|Linker.objects.filter(id__iexact=item.id)
    
    return filtered_list

def hydroselect(hydro_slection):
    hydrophobicity_items=Hydrophobicity.objects.none()
    for i in hydro_slection:
        if i=='Extremely Hydrophobic':
            hydrophobicity_items=hydrophobicity_items|Hydrophobicity.objects.filter(gravy_score__gt=1) 
        if i=='Hydrophobic':
            hydrophobicity_items=hydrophobicity_items|Hydrophobicity.objects.filter(gravy_score__range=(0.5,1))
        if i=='Moderate':
            hydrophobicity_items=hydrophobicity_items|Hydrophobicity.objects.filter(gravy_score__range=(-0.5,0.5)) 
        if i=='Hydrophilic':
            hydrophobicity_items=hydrophobicity_items|Hydrophobicity.objects.filter(gravy_score__range=(-1,-0.5)) 
        if i=='Extremely Hydrophilic':
            hydrophobicity_items=hydrophobicity_items|Hydrophobicity.objects.filter(gravy_score__lt=-1)

    filtered_list = Linker.objects.none() 
    for item in hydrophobicity_items:
        filtered_list=filtered_list |Linker.objects.filter(id__iexact=item.id)
    return filtered_list
                
def multiselect(request):
    if request.method=='POST':
        length_selection=request.POST.getlist('lengths')
        flexibility_selection=request.POST.getlist('Flexibility')
        hydrophobicity_selection=request.POST.getlist('Hydrophobicity')
    else:
        length_selection=[]
        flexibility_selection=[]
        hydrophobicity_selection=[]
    
    
    length_selected_items=Linker.objects.none()
    if len(length_selection)>0:
        length_selected_items=lengthselect(length_selection)
        print(length_selected_items)

    if len(flexibility_selection)>0:
        flex_selected_items=flexselect(flexibility_selection)
        print(flex_selected_items)

    if len(hydrophobicity_selection)>0:
        hydrophobicity_items=hydroselect(hydrophobicity_selection)
        print(hydrophobicity_items)
    

    queryset=length_selected_items.intersection(flex_selected_items)
    queryset=queryset.intersection(hydrophobicity_items)

    context = {
        'selected_items': queryset
    }

    return render(request,'results.html',context)

def backbone_dyna(seq):
    url = 'https://bio2byte.be/msatools/api/'
    token = "flexibility"
    #values = {'tool_list': ['dynamine'], 'token': token}

    r = requests.post(url, data={1: seq})
    queue_url = json.loads(r.content.decode("utf-8"))['Location']
    queue_status_url = 'https://bio2byte.be/msatools' + queue_url

    while True:
        response = requests.get(queue_status_url)
        if response.status_code == 200:
            response = requests.get(queue_status_url)
            r=response.json()
            #print("HTTP Status: 200 OK")
            break  # Exit the loop once status is 200
        else:
            #print(f"HTTP Status: {response.status_code}")
            time.sleep(10)  # Delay for 10 seconds before checking again

    backbone=r['results'][0]['backbone']
    average=sum(backbone)/len(backbone)
    results={'backbone':str(backbone),'average':average}

    return results

# Given functions hydrophobicity_calculator and hydrophobicity_distribution
def hydrophobicity_calculator(sequence, ph_env):
    # Acidic Environment (pH2)
    hydrophobicity_1a = {"L":100, "I":100, "F":92, "W":84, "V":79, "M":74}
    hydrophobicity_2a = {"C":52, "Y":49, "A":47}
    hydrophobicity_3a = {"T":13, "E":8, "G":0, "S":-7, "Q":-18, "D":-18}
    hydrophobicity_4a = {"R":-26, "K":-37, "N":-41, "H":-42, "P":-46}

    # Neutral Environment (pH7)
    hydrophobicity_1n = {"F":100, "I":99, "W":97, "L":97, "V":76, "M":74}
    hydrophobicity_2n = {"Y":63, "C":49, "A":41}
    hydrophobicity_3n = {"T":13, "H":8, "G":0, "S":-7, "Q":-10}
    hydrophobicity_4n = {"R":-14, "K":-23, "N":-28, "P":-46, "D":-55}

    i = 0
    vhydrophobic = 0
    hydrophobic = 0
    neutral = 0
    hydrophilic = 0

    for i in sequence: 
        if ph_env.lower() == ("acidic"):
            if i in (hydrophobicity_1a):
                vhydrophobic += 1 
            elif i in (hydrophobicity_2a):
                hydrophobic += 1 
            elif i in (hydrophobicity_3a):
                neutral += 1 
            elif i in (hydrophobicity_4a):
                hydrophilic += 1 
        
        if ph_env.lower() == ("neutral"):
            if i in (hydrophobicity_1n):
                vhydrophobic += 1 
            elif i in (hydrophobicity_2n):
                hydrophobic += 1 
            elif i in (hydrophobicity_3n):
                neutral += 1 
            elif i in (hydrophobicity_4n):
                hydrophilic += 1 

    percent_vhydrophobic = (vhydrophobic/(vhydrophobic + hydrophobic + neutral + hydrophilic)*100)
    percent_hydrophobic = (hydrophobic/(vhydrophobic + hydrophobic + neutral + hydrophilic)*100)
    percent_neutral = (neutral/(vhydrophobic + hydrophobic + neutral + hydrophilic)*100)
    percent_hydrophilic = (hydrophilic/(vhydrophobic + hydrophobic + neutral + hydrophilic)*100)

    results = {
        "Very Hydrophobic": percent_vhydrophobic,
        "Hydrophobic": percent_hydrophobic,
        "Neutral": percent_neutral,
        "Hydrophilic": percent_hydrophilic
    }

    return results

def hydrophobicity_distribution(sequence, ph_env):
    # Defining the hydrophobicity values based on environment
    if ph_env.lower() == "acidic":
        # Acidic Environment (pH2)
        letters = {"L":100, "I":100, "F":92, "W":84, "V":79, "M":74, "C":52, "Y":49, "A":47, "T":13, "E":8, "G":0, "S":-7, "Q":-18, "D":-18, "R":-26, "K":-37, "N":-41, "H":-42, "P":-46}
    elif ph_env.lower() == "neutral":
        # Neutral Environment (pH7)
        letters = {"F":100, "I":99, "W":97, "L":97, "V":76, "M":74, "Y":63, "C":49, "A":41, "T":13, "H":8, "G":0, "S":-7, "Q":-10, "R":-14, "K":-23, "N":-28, "P":-46, "D":-55}

    # Define the RGB values for the colormap
    colors1 = [(0.0, 0.0, 0.5),  # Blue
            (1.0, 1.0, 1.0)]  # White

    colors2 = [(1.0, 1.0, 1.0),  # White
            (0.9, 0.55, 0.0)]  # Yellow-Orange

    # Defining map distribution
    dis1 = 0.355
    dis2 = 0.645

    # Create the two parts of the colormap
    cmap1 = plt.cm.colors.LinearSegmentedColormap.from_list('cmap1', colors1)
    cmap2 = plt.cm.colors.LinearSegmentedColormap.from_list('cmap2', colors2)

    # Combine the two parts into a single colormap
    cmap = plt.cm.colors.LinearSegmentedColormap.from_list('custom_cmap', [cmap1(i / int(dis1 * 256)) for i in range(int(dis1 * 256))] +
                                            [cmap2((i - int(dis1 * 256)) / int(dis2 * 256)) for i in
                                            range(int(dis1 * 256), int(dis1 * 256) + int(dis2 * 256))])
    
    # Create a figure and axes
    fig, ax = plt.subplots(figsize=(len(sequence) * 0.5, 1))

    # Iterate over the letters in the text input and create colored rectangles
    x = 0
    for letter in sequence:
        # Get the value for the letter from the letters dictionary
        value = letters.get(letter, 0)

        # Normalize the value to the range [0, 1]
        normalized_value = (value - min(letters.values())) / (max(letters.values()) - min(letters.values()))

        # Set the color based on the value range using the colormap
        color = cmap(normalized_value)

        rect = plt.Rectangle((x, 0), 1, 1, color=color)
        ax.add_artist(rect)

        ax.text(x + 0.5, 0.5, letter, color='black',
                fontsize=12, ha='center', va='center')

        x += 1

    # Customize the plot
    ax.set_xlim(0, len(sequence))
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Save the plot to a BytesIO buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0)
    buffer.seek(0)
    
    # Encode the image data using Base64
    img_data = base64.b64encode(buffer.read()).decode('utf-8')
    
    # Close the plot to free up resources
    plt.close()

    return img_data

def gravy(sequence):
    # Kyte-Doolittle hydropathy scale values for amino acids
    hydropathy_values = {
        'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5,
        'C': 2.5, 'Q': -3.5, 'E': -3.5, 'G': -0.4,
        'H': -3.2, 'I': 4.5, 'L': 3.8, 'K': -3.9,
        'M': 1.9, 'F': 2.8, 'P': -1.6, 'S': -0.8,
        'T': -0.7, 'U': 0.0, 'W': -0.9, 'Y': -1.3,
        'V': 4.2
    }
    
    # Calculate the GRAVY score
    total_hydropathy = sum(hydropathy_values.get(aa, 0) for aa in sequence)
    gravy_score = total_hydropathy / len(sequence)
    
    return gravy_score

def add_linker(request):
    submitted=False
    
    if request.method=="POST":
        
        form=LinkerForm(request.POST,prefix='form1') #fill out the form and they are posted
        form2=FlexForm(request.POST,prefix='form2')
        
        
        if form.is_valid() & form2.is_valid():
            
            instance=form.save()
            id=instance.id
            print("ID in POST:", id)
            #instance2=form2.save()
            flexibility_data=flexibility(id=instance.id,Sequence=instance.aasequence,backbone=backbone_dyna(instance.aasequence)['backbone'],average_flexibility=backbone_dyna(instance.aasequence)['average'],type=form2.cleaned_data.get('type'))

            if flexibility_data.type=='unknown':
                if flexibility_data.average_flexibility<=0.69:
                    flexibility_data.type='flexible'
                    flexibility_data.save()
                elif flexibility_data.average_flexibility>=0.8:
                    flexibility_data.type='rigid'
                    flexibility_data.save()
                else:
                    flexibility_data.type='context dependent (can be either flexible or rigid)'
                    flexibility_data.save()


            acidic_res=hydrophobicity_calculator(instance.aasequence,'acidic')
            neu_res=hydrophobicity_calculator(instance.aasequence,'neutral')
            Hydrophobicity_data=Hydrophobicity(id=instance.id,sequence=instance.aasequence,acidic_very_hydrophobic=acidic_res['Very Hydrophobic'],acidic_hydrophobic=acidic_res['Hydrophobic'],acidic_neutral=acidic_res['Neutral'],acidic_hydrophilic=acidic_res['Hydrophilic'],neutral_very_hydrophobic = neu_res['Very Hydrophobic'],neutral_hydrophobic = neu_res['Hydrophobic'],neutral_neutral = neu_res['Neutral'],neutral_hydrophilic = neu_res['Hydrophilic'],gravy_score=gravy(instance.aasequence),acidic_img_data=hydrophobicity_distribution(instance.aasequence,'acidic'),neutral_img_data=hydrophobicity_distribution(instance.aasequence,'neutral'))
            
            Hydrophobicity_data.save()
            flexibility_data.save()
            form.save()
            
            
            return HttpResponseRedirect(f'?submitted=True&id={instance.id}') #sending it to the get request
            #return HttpResponseRedirect(reverse('add_venue') + '?submitted=True')
        id=instance.id
        print("ID in POST:", id)
        
    else:
        form=LinkerForm(prefix='form1') 
        form2=FlexForm(prefix='form2')
        
        if "submitted" in request.GET:
            submitted=True
        


    return render(request,'linkerform.html',{'form1':form,'form2':form2,'submitted':submitted})