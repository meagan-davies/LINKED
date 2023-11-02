import requests, json,time
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect,HttpRequest,HttpResponse
import sys  
from django.views.generic import ListView
from django.db.models import Q # new
from django.shortcuts import render
import ast
import pandas as pd
import plotly.express as px
from plotly.offline import plot
from .forms import CalcForm

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import io
import base64
from PIL import Image
from io import BytesIO


def search_view(request):
    return render(request, 'calc.html')



# post request to recieve data from the server

def flex_calc(seq):
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
        "Very_Hydrophobic": percent_vhydrophobic,
        "Hydrophobic": percent_hydrophobic,
        "Neutral": percent_neutral,
        "Hydrophilic": percent_hydrophilic
    }

    return results

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

def graph_flex(sequence,backbone):
    if len(sequence) >=5: 
            #conver the list of strings to numbers
            char_list = ast.literal_eval(backbone)    

            #index amino acid
            index_list=[]
            for i in range(1,len(sequence)+1):
                index=sequence[i-1]+str(i)
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
            return dynamic_plot
    else:
        return "This is likely a rigid linker"
    
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

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches='tight', pad_inches=0)
    plt.close(fig)  # Close the figure to free up resources

    # Convert the image buffer to a base64-encoded string
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    return image_base64


def calc(request: HttpRequest) -> HttpResponse: 
    amino_acid = ['A', 'C', 'D', 'E','F','G','H','I','K','M','N','P','Q','R','S','T','V','W','Y','L']
    
    if request.method == "GET":
        form = CalcForm()
    elif request.method == "POST":
        form = CalcForm(request.POST)
        if form.is_valid():
            sequence=form.cleaned_data['sequence']

            if not all(letter in amino_acid for letter in sequence):
                form.add_error('sequence', 'This is not a valid sequence, please try again')

            else:        
                flex_res=flex_calc(sequence)
                acidic_hydro_res=hydrophobicity_calculator(sequence,'acidic')
                neutral_hydro_res=hydrophobicity_calculator(sequence,'neutral')
                gravy_score=gravy(sequence)
                plot=graph_flex(sequence,flex_res['backbone'])
                length=len(sequence)
                ac_hydro_graph=hydrophobicity_distribution(sequence,'acidic')
                neu_hydro_graph=hydrophobicity_distribution(sequence,'neutral')
            

                context={
                    'sequence':sequence,
                    'flex':flex_res,
                    'acidic_hydro':acidic_hydro_res,
                    'neutral_hydro':neutral_hydro_res,
                    'gravy_score':gravy_score,
                    'plot':plot,
                    'length': length,
                    'acidic_graph':ac_hydro_graph,
                    'neu_hydro_graph': neu_hydro_graph
                }
        
                return render(request, "calc.html", {"context": context, "success": True})
    else:
        raise NotImplementedError
    
    return render(request, "calc.html", {"form": form})



