import pandas as pd 
import plotly.graph_objs as go
import nltk
import unicodedata
import re
from wordcloud import WordCloud, STOPWORDS
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import flask
import dash
import dash_table
import dash_auth



VALID_USERNAME_PASSWORD_PAIRS = {
    'erasmus': 'sn$%54$%'
}

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
df = pd.read_csv('data/all_description.csv')
country_job_counts_df= pd.read_csv('data/job_counts_country.csv')
bigram_df = pd.read_csv('data/bigrams.csv')
top_companies_df = pd.read_csv('data/recruiters_by_jobposting.csv',names=['Company','Counts'])
map_token = 'pk.eyJ1IjoidmFzaWxpc250b3VzaXMiLCJhIjoiY2tjaHViMW1lMTVjaDJ6bm5kNW4xZHZ5NCJ9.nSmlFX-NDiWfenQAhE8c3Q'

ADDITIONAL_STOPWORDS = ['this','security','look','with','look','forward','your','more','than','this position','more','cyber security','information security','working with','look forward','your application','forward','receiving','experience with','this position','years','experience','cyber','role','credit','suisse','flexible','working','work','closely','good','knowledge','information','technology','best','must','help','including','cantidate','relevant','within','provide','reqiuired','strong','please','student','candidate','deloitte','position','able','und','die','mit','un','wir','fr','join','u','give','unsere','mitarbeitenden','region', 'zurichzurich','united','nation','your application','well'
]
def basic_clean(text):
  """
  A simple function to clean up the data. All the words that
  are not designated as a stop word is then lemmatized after
  encoding and basic regex parsing are performed.
  """
  wnl = nltk.stem.WordNetLemmatizer()
  stopwords = nltk.corpus.stopwords.words('english') + ADDITIONAL_STOPWORDS
  text = (unicodedata.normalize('NFKD', text)
    .encode('ascii', 'ignore')
    .decode('utf-8', 'ignore')
    .lower())
  words = re.sub(r'[^\w\s]', '', text).split()
  return [wnl.lemmatize(word) for word in words if word not in stopwords]


df['Description'] = df['Description'].apply(basic_clean)



for stopword in ADDITIONAL_STOPWORDS:
    STOPWORDS.add(stopword)






def plotly_wordcloud(dataframe):
    description_text = list(dataframe['Description'].dropna().values)
    text = " ".join(str(x) for x in description_text)
    word_cloud = WordCloud(stopwords=set(STOPWORDS),max_words=100,max_font_size=90,scale=1)
    word_cloud.generate(text)

    word_list = []
    freq_list = []
    fontsize_list = []
    position_list = []
    orientation_list = []
    color_list = []

    for (word, freq), fontsize, position, orientation, color in word_cloud.layout_:
        word_list.append(word)
        freq_list.append(freq)
        fontsize_list.append(fontsize)
        position_list.append(position)
        orientation_list.append(orientation)
        color_list.append(color)
    
    print(position_list)
    x_arr = []
    y_arr = []
    for i in position_list:
        x_arr.append(i[0])
        y_arr.append(i[1])

    # get the relative occurence frequencies
    new_freq_list = []
    for i in freq_list:
        new_freq_list.append(i * 80)

    trace = go.Scatter(
        x=x_arr,
        y=y_arr,
        textfont=dict(size=new_freq_list, color=color_list),
        hoverinfo="text",
        textposition="top center",
        hovertext=["{0} - {1}".format(w, f) for w, f in zip(word_list, freq_list)],
        mode="text",
        text=word_list,)

    layout = go.Layout(
            {
                "xaxis": {
                    "showgrid": False,
                    "showticklabels": False,
                    "zeroline": False,
                    "automargin": True,
                    "range": [-100, 250],
                },
                "yaxis": {
                    "showgrid": False,
                    "showticklabels": False,
                    "zeroline": False,
                    "automargin": True,
                    "range": [-100, 450],
                },
                "margin": dict(t=20, b=20, l=10, r=10, pad=4),
                "hovermode": "closest",
            }
        )

    wordcloud_figure_data = {"data": [trace], "layout": layout}
    word_list_top = word_list[:25]
    word_list_top.reverse()
    freq_list_top = freq_list[:25]
    freq_list_top.reverse()

    frequency_figure_data = {
        "data": [
            {
                "y": word_list_top,
                "x": freq_list_top,
                "type": "bar",
                "name": "",
                "orientation": "h",
            }
        ],
        "layout": {"height": "550", "margin": dict(t=20, b=20, l=100, r=20, pad=4)},
    }
    treemap_trace = go.Treemap(
        labels=word_list_top, parents=[""] * len(word_list_top), values=freq_list_top
    )
    treemap_layout = go.Layout({"margin": dict(t=10, b=10, l=5, r=5, pad=4)})
    treemap_figure = {"data": [treemap_trace], "layout": treemap_layout}
    return wordcloud_figure_data, frequency_figure_data, treemap_figure


NAVBAR = dbc.Navbar(
    children=[
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(
                        dbc.NavbarBrand("Cyber Security Jobs", className="ml-2")
                    ),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://plot.ly",
        )
    ],
    color="dark",
    dark=True,
    sticky="top",
)

TOP_COMPANIES_PLOT = [
    dbc.CardHeader(html.H5("Top 20 companies by number of jobs posting")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-company-hist",
                children=[
                    dbc.Alert(
                        "Not enough data to render this plot, please adjust the filters",
                        id="no-data-alert-company",
                        color="warning",
                        style={"display": "none"},
                    ),
                    dcc.Graph(id="company-sample"),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]


WORDCLOUD_PLOTS = [
    dbc.CardHeader(html.H5("Most frequently used words in jobs description")),
    dbc.Alert(
        "Not enough data to render these plots, please adjust the filters",
        id="no-data-alert",
        color="warning",
        style={"display": "none"},
    ),
    dcc.Dropdown(
            id="job-drop", options= [{'label': 'Test','value':'A'}],value='Test',clearable=False, style={"marginBottom": 50, "font-size": 12}
        ),
     
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Loading(
                            id="loading-frequencies",
                            children=[dcc.Graph(id="frequency_figure")],
                            type="default",
                        )
                    ),
                    dbc.Col(
                        [
                            dcc.Tabs(
                                id="tabs",
                                children=[
                                    dcc.Tab(
                                        label="Treemap",
                                        children=[
                                            dcc.Loading(
                                                id="loading-treemap",
                                                children=[dcc.Graph(id="job-treemap")],
                                                type="default",
                                            )
                                        ],
                                    ),
                                    dcc.Tab(
                                        label="Wordcloud",
                                        children=[
                                            dcc.Loading(
                                                id="loading-wordcloud",
                                                children=[
                                                    dcc.Graph(id="job-wordcloud")
                                                ],
                                                type="default",
                                            )
                                        ],
                                    ),
                                ],
                            )
                        ],
                        md=8,
                    ),
                ]
            )
        ]
    ),
]

TOP_BIGRAM_PLOT = [
    dbc.CardHeader(html.H5("Top bigrams found in the database")),
     dbc.CardBody(
        [
            dcc.Loading(
                id="loading-bigrams-scatter",
                children=[
                    dbc.Alert(
                        "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                        id="no-data-alert-bigrams",
                        color="warning",
                        style={"display": "none"},
                    ),
                     dcc.Graph(id="bigrams-scatter"),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]






GEO_MAP_PLOTS  = [
    dbc.CardHeader(html.H5('Job Counts per Country')),dbc.CardBody(
        [
            dcc.Loading(
                id="loading-geomap",
                children=[
                    dbc.Alert(
                        "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                        id="no-data-alert-geomap",
                        color="warning",
                        style={"display": "none"},
                    ),
                     dcc.Graph(id="geomap"),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

BODY = dbc.Container([dbc.Card(WORDCLOUD_PLOTS),dbc.Card(TOP_BIGRAM_PLOT),dbc.Card(TOP_COMPANIES_PLOT ),dbc.Card(GEO_MAP_PLOTS),])
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
app.layout = html.Div(children=[NAVBAR, BODY])

@app.callback(
  [
        Output("job-wordcloud", "figure"),
        Output("frequency_figure", "figure"),
        Output("job-treemap", "figure"),
        Output("no-data-alert", "style"),
    ],
    [Input('job-drop',"value")],
)

def generate_wordcloud_graph(x):
    wordcloud, frequency_figure,treemap = plotly_wordcloud(df)
    alert_style = {'display': 'none'}
    return (wordcloud, frequency_figure, treemap, alert_style)

@app.callback(
    
Output('bigrams-scatter','figure'), 
[Input('job-drop',"value")],)

def populate_bigram_scatter(x):
    fig = px.scatter(
        bigram_df,
        x= 'Word',
        y='Frequency',
        hover_name='Word',
        text = 'Word',
        size='Frequency',
        color='Word',
        size_max=45,
        template='plotly_white',
        title="Bigram similarity and frequency",
        color_continuous_scale=px.colors.sequential.Sunsetdark,

    )
    fig.update_traces(marker=dict(line=dict(width=1, color="Gray")))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig

@app.callback(
    [Output('company-sample','figure'),Output("no-data-alert-company", "style")],
    [Input('job-drop','value')],)
def top_companies_histogram(x):
    top_20_companies = top_companies_df[0:20]
    data = [
        {'x':top_20_companies['Company'],
        'y':top_20_companies['Counts'],
        'text': top_20_companies['Company'],
        "textposition": "auto",
        "type": "bar",
        "name": "",
        }
    ]
    layout = {
        "autosize": False,
        "margin": dict(t=15, b=10, l=40, r=0, pad=4),
        "xaxis": {"showticklabels": False},
    }

    return [{"data": data, "layout": layout}, {"display": "none"}]
    
@app.callback(
    Output('geomap','figure'),
    [Input('job-drop','value')],
)
def generate_map (x):
    fig=go.Figure()
    fig.add_trace(go.Choropleth(
        locationmode='country names',
        locations = country_job_counts_df['Country'],
        z= country_job_counts_df['JobCounts'],
        text= country_job_counts_df['Country'],
        colorscale = [[0,'rgb(0, 0, 0)'],[1,'rgb(0, 0, 0)']],
        autocolorscale = False,
        showscale = False,
        geo = 'geo2',
        
        )),
    fig.add_trace(go.Scattergeo(
        lon = [15.820312500000002],
        lat = [49.38237278700955],
        text = ['Europe'],
        mode = 'text',
        showlegend = False,
        geo = 'geo2'
        
    ))

    fig.update_layout(
    title = go.layout.Title(
        text = 'Jobs per Country'),
        geo = go.layout.Geo(
            resolution = 50,
            scope = 'europe',
            showframe = False,
            showcoastlines = True,
            landcolor = "rgb(111, 111, 111)",
            countrycolor = "white" ,
            coastlinecolor = "white",
            lonaxis_range= [ -15.0, -5.0 ],
            lataxis_range= [ 0.0, 12.0 ],
            domain = dict(x = [ 0, 1 ], y = [ 0, 1 ]),
            
             
            
           
            
    ),
    geo2 = go.layout.Geo(
        scope = 'europe',
        showframe = False,
        landcolor = "rgb(229, 229, 229)",
        showcountries = False,
        domain = dict(x = [ 0, 0.6 ], y = [ 0, 0.6 ]),
        bgcolor = 'rgba(255, 255, 255, 0.0)',
        
      
        
    ),
    legend_traceorder = 'reversed',
    )
    return fig
    



if __name__ == "__main__":
    app.run_server(debug=True)