import pandas as pd
import os
from matplotlib import style
import matplotlib.dates as mdates
import json
import plotly
import plotly.express as px
style.use('ggplot')
import copy
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date
from datetime import timedelta
import datetime
from pytz import timezone
import ssl
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from urllib.request import urlopen as uReq
ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)  # initialising the flask app with the name 'app'
CORS(app)
@app.route('/', methods=['GET'])
@cross_origin()
def homepage():
    head='India'
    head=head.upper()
    today = pd.to_datetime(datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f'))
    curr_datetime=today.strftime("%d/%m/%Y, %H:%M")
    curr_date=today.day
    curr_month=today.month
    curr_hour=today.hour
    path1 = 'https://data.covid19bharat.org/csv/latest/states.csv'
    data = pd.read_csv(path1)
    data['Date'] = pd.to_datetime(data['Date'])
    data_india = copy.deepcopy(data[data['State'] == 'India'])
    data_india = data_india.reset_index(drop=True)
    d1 = copy.deepcopy(data_india[-101:])
    d1 = d1.reset_index(drop=True)
    d1['Date'] = pd.to_datetime(d1['Date'])
    india_wise_data_total_cases = []
    india_wise_data_total_deaths = []
    india_wise_data_daily_new_cases = []
    india_wise_data_daily_new_deaths = []
    india_wise_data_daily_tests = []
    india_wise_data_total_tests=[]
    india_wise_data_daily_tpr = []

    os.system("")

    # Group of Different functions for different styles

    for i in range(1, len(d1)):
        india_wise_data_daily_new_cases.append(d1['Confirmed'][i] - d1['Confirmed'][i - 1])
        india_wise_data_daily_new_deaths.append(d1['Deceased'][i] - d1['Deceased'][i - 1])
        india_wise_data_daily_tests.append(d1['Tested'][i]-d1['Tested'][i-1])
        india_wise_data_total_tests.append(d1['Tested'][i])
        india_wise_data_total_cases.append(d1['Confirmed'][i])
        india_wise_data_total_deaths.append(d1['Deceased'][i])
        try:
            tpr=100*(d1['Confirmed'][i] - d1['Confirmed'][i - 1])/(d1['Tested'][i]-d1['Tested'][i-1])
        except:
            tpr=0
        india_wise_data_daily_tpr.append(tpr)

    tot_cases = int(india_wise_data_total_cases[-1])
    # print(f"{tot_cases:,}")
    tot_deaths = int(india_wise_data_total_deaths[-1])
    # print(f"{tot_deaths:,}")
    tot_tests=int(india_wise_data_total_tests[-1])
    new_cases = int(india_wise_data_daily_new_cases[-1])
    new_deaths = int(india_wise_data_daily_new_deaths[-1])
    new_tests=int(india_wise_data_daily_tests[-1])

    change_in_24hr_cases = int(india_wise_data_daily_new_cases[-2] - india_wise_data_daily_new_cases[-3])
    try:
        per_change_in_24hr_cases = 100 * (india_wise_data_daily_new_cases[-2] - india_wise_data_daily_new_cases[-3]) / \
                                   india_wise_data_daily_new_cases[-3]
    except:
        per_change_in_24hr_cases=0
    change_in_week_cases = int(india_wise_data_daily_new_cases[-2] - india_wise_data_daily_new_cases[-9])
    try:

        per_change_in_week_cases = 100 * (india_wise_data_daily_new_cases[-2] - india_wise_data_daily_new_cases[-9]) / \
                               india_wise_data_daily_new_cases[-9]
    except:
        per_change_in_week_cases=0
    change_in_month_cases = int(india_wise_data_daily_new_cases[-2] - india_wise_data_daily_new_cases[-32])
    try:

        per_change_in_month_cases = 100 * (india_wise_data_daily_new_cases[-2] - india_wise_data_daily_new_cases[-32]) / \
                                india_wise_data_daily_new_cases[-32]
    except:
        per_change_in_month_cases=0

    cases_yesterday = int(india_wise_data_daily_new_cases[-2])
    deaths_yesterday = int(india_wise_data_daily_new_deaths[-2])
    tests_yesterday=int(india_wise_data_daily_tests[-2])
    try:
        TPR_yesterday=round(100*cases_yesterday/tests_yesterday,2)
    except:
        TPR_yesterday=0
    try:
        TPR_Week=round(100*india_wise_data_daily_new_cases[-8]/india_wise_data_daily_tests[-8],2)
    except:
        TPR_Week=0
    try:
        TPR_Month = round(100 * india_wise_data_daily_new_cases[-31] / india_wise_data_daily_tests[-31], 2)
    except:
        TPR_Month=0
    datetime_last = pd.to_datetime(d1.iloc[-1:, :]['Date'].values)
    if curr_hour>=16 and curr_date<=23:
        delta_case=new_cases
        delta_deaths=new_deaths
        delta_tests=new_tests
    else:
        delta_case=cases_yesterday
        delta_deaths=deaths_yesterday
        delta_tests=tests_yesterday

    # print(datetime_last)
    date_last = datetime_last.day
    date_month = datetime_last.month
    date_year = datetime_last.year
    month_num = str(date_month[0])
    datetime_object = datetime.datetime.strptime(month_num, "%m")
    date_month = datetime_object.strftime("%b")
    # print("Short name: ",date_month)
    final_date = str(date_last[0]) + " " + str(date_month) + " " + str(date_year[0])
    # print(final_date)
    line1="Total COVID-19 Cases as of {} : {} (+ {} )".format(final_date, f"{tot_cases:,}",delta_case)
    line2 = "Total COVID-19 Related Deaths as of {} : {} (+ {} ) ".format(final_date, f"{tot_deaths:,}",delta_deaths)
    line0 = "Total Number of Samples Tested for COVID-19 as of {} : {} (+ {} ) ".format(final_date, f"{tot_tests:,}", delta_tests)
    line3 = "NEW COVID-19 Cases Today: {}".format(f"{new_cases:,}")
    line4 = "NEW COVID-19 Deaths Today : {}".format(f"{new_deaths:,}")

    line5 = "COVID-19 Cases Yesterday: {}".format(f"{cases_yesterday:,}")
    line6 = "COVID-19 Deaths Yesterday: {}".format(f"{deaths_yesterday:,}")
    line13="Total Positivity Rate Yesterday: {}%".format(TPR_yesterday)

    line7 = "Increase/Decrease in Cases in last 24hrs: {}".format(f"{change_in_24hr_cases:,}")

    line8 = "Percentage Increase/Decrease in Cases in last 24hrs: {}%".format(round(per_change_in_24hr_cases, 2))

    line9 = "Increase/Decrease in A Week: {}".format(f"{change_in_week_cases:,}")
    line10 = "Percentage Increase/Decrease in a Week: {}%".format(round(per_change_in_week_cases, 2))
    line14="Total Positivity Rate Last Week: {}% ".format(TPR_Week)

    line11 = "Increase/Decrease in a Month: {}".format(f"{change_in_month_cases:,}")
    line12 = "Percentage Increase/Decrease in A Month: {}%".format(round(per_change_in_month_cases, 2))
    line15 = "Total Positivity Rate Last Month: {}% ".format(TPR_Month)


    # plot1
    df = pd.DataFrame()
    df['Date'] = d1['Date'][1:100]
    print(len(df))
    df['Date'] = pd.to_datetime(d1['Date'])
    df['Deaths'] = india_wise_data_daily_new_deaths[:-1]
    df['Number of COVID-19 Cases'] = india_wise_data_daily_new_cases[:-1]
    fig = px.bar(df, x='Date', y='Number of COVID-19 Cases', color='Deaths',
                 color_continuous_scale=px.colors.sequential.YlOrRd, hover_data={"Date": "|%d, %b, %Y"},
                 title='Number of COVID-19 Cases and Deaths in India')
    fig.update_xaxes(dtick="M1", tickformat="%b\n%Y")
    fig.update_layout(paper_bgcolor="lightblue")

    graphJSON1 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    df=None
    fig=None

    # PLOT 2
    df = pd.DataFrame()
    df['Date'] = d1['Date'][1:100]
    df['Date'] = pd.to_datetime(d1['Date'])
    df['Number of Samples Tested'] = india_wise_data_daily_tests[:-1]
    df['TPR'] = india_wise_data_daily_tpr[:-1]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(x=df['Date'], y=df['Number of Samples Tested'], name="Daily Tests",
               hovertemplate='Date: %{x|%d, %b, %Y} <br> Tests: %{y:d}<extra></extra>'),
        secondary_y=False, )
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['TPR'], name="Positivity Rate (%)",
                   hovertemplate='Date: %{x|%d, %b, %Y} <br> Positivity: %{y:.2f}%<extra></extra>'),
        secondary_y=True, )
    fig.update_layout(
        title_text="Daily COVID-19 Tests and Positivity Rate",paper_bgcolor="lightcyan")
    fig.update_xaxes(title_text="Time")
    fig.update_xaxes(dtick="M1", tickformat="%b\n%Y")
    fig.update_yaxes(title_text="<b>Number of Samples Tested</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Positivity Rate</b>(in %)", secondary_y=True)
    graphJSON2 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # all states analysis

    date_today = max(data['Date'])
    date_100 = date_today - timedelta(days=16)
    d1 = copy.deepcopy(data[data['Date'] > date_100])
    d1 = d1.reset_index(drop=True)
    index = 1
    cases_week = {}
    deaths_week = {}
    states = d1['State'].unique()
    for j in range(0, len(states)):
        if states[j] == "India" or states[j] == "State Unassigned":
            continue;
        d = copy.deepcopy(d1[d1['State'] == states[j]])
        d = d.reset_index(drop=True)
        #     print(d)
        new_cases = []
        new_cases.append(0)
        new_recovery = []
        new_recovery.append(0)
        new_deaths = []
        new_deaths.append(0)
        new_tests = []
        new_tests.append(0)
        for i in range(0, len(d) - 1):
            new_cases.append(d['Confirmed'].values[i + 1] - d['Confirmed'].values[i])
            new_recovery.append(d['Recovered'].values[i + 1] - d['Recovered'].values[i])
            new_deaths.append(d['Deceased'].values[i + 1] - d['Deceased'].values[i])
            new_tests.append(d['Tested'].values[i + 1] - d['Tested'].values[i])
        d['new_cases'] = new_cases
        d['new_recovery'] = new_recovery
        d['new_deaths'] = new_deaths
        d['new_tests'] = new_tests
        cases_w = 0
        deaths_w = 0
        for i in range(9, 15):
            cases_w += d['new_cases'].values[i]
            deaths_w += d['new_deaths'].values[i]
        cases_week[states[j]] = cases_w
        deaths_week[states[j]] = deaths_w
    data_cases_week = pd.DataFrame(sorted(cases_week.items(), key=lambda x: x[1], reverse=True))
    data_cases_week.columns = ['State', 'Cases In a Week']
    data_deaths_week = pd.DataFrame(sorted(deaths_week.items(), key=lambda x: x[1], reverse=True))
    data_deaths_week.columns = ['State', 'Deaths In a Week']
    data_states_week = data_cases_week.merge(data_deaths_week, on='State')
    dic = {'Dadra and Nagar Haveli and Daman and Diu': 'Dadra & N.H & Daman & Diu',
           'Andaman and Nicobar Islands': 'Andaman & N. Islands'}
    data_states_week['States/UTs'] = data_states_week['State'].replace(dic)

    #
    # plot 3

    fig3 = px.bar(data_states_week, x='States/UTs', y='Cases In a Week', color='Deaths In a Week',
                 color_continuous_scale=px.colors.sequential.Burg, title='Cases and Deaths in States/UTs of India in a Week')
    fig3.update_layout(autosize=False,
                      width=1000,
                      height=600,
                      paper_bgcolor="LightSteelBlue",
                      )
    fig = None
    graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)




    return render_template('home1.html',head=head,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6,line7=line7,line8=line8,line9=line9,line10=line10,line11=line11,line12=line12,curr_datetime=curr_datetime,line0=line0,line13=line13,line14=line14,line15=line15,graphJSON1=graphJSON1,graphJSON2=graphJSON2,graphJSON3=graphJSON3)

@app.route('/state', methods=['POST'])
def dropdown():
    if (request.method=='POST'):
        input_state=request.form['operation']
    today = pd.to_datetime(datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f'))
    curr_datetime = today.strftime("%d/%m/%Y, %H:%M")
    curr_date = today.day
    curr_month = today.month
    curr_hour = today.hour
    path1 = 'https://data.covid19bharat.org/csv/latest/states.csv'
    data = pd.read_csv(path1)
    data_state = data[data['State'] == input_state]
    data_state = data_state.reset_index(drop=True)
    d1 = copy.deepcopy(data_state[-101:])
    d1 = d1.reset_index(drop=True)
    d1['Date'] = pd.to_datetime(d1['Date'])
    state_wise_data_total_cases = []
    state_wise_data_total_deaths = []
    state_wise_data_daily_new_cases = []
    state_wise_data_daily_new_deaths = []
    state_wise_data_daily_tests = []
    state_wise_data_total_tests = []
    state_wise_data_daily_tpr = []

    for i in range(1, len(d1)):
        state_wise_data_daily_new_cases.append(d1['Confirmed'][i] - d1['Confirmed'][i - 1])
        state_wise_data_daily_new_deaths.append(d1['Deceased'][i] - d1['Deceased'][i - 1])
        state_wise_data_daily_tests.append(d1['Tested'][i] - d1['Tested'][i - 1])
        state_wise_data_total_tests.append(d1['Tested'][i])
        state_wise_data_total_cases.append(d1['Confirmed'][i])
        state_wise_data_total_deaths.append(d1['Deceased'][i])
        try:
            tpr = 100 * (d1['Confirmed'][i] - d1['Confirmed'][i - 1]) / (d1['Tested'][i] - d1['Tested'][i - 1])
        except:
            trp=0
        state_wise_data_daily_tpr.append(tpr)

    tot_cases = int(state_wise_data_total_cases[-1])
    # print(f"{tot_cases:,}")
    tot_deaths = int(state_wise_data_total_deaths[-1])
    # print(f"{tot_deaths:,}")
    tot_tests = int(state_wise_data_total_tests[-1])
    new_cases = int(state_wise_data_daily_new_cases[-1])
    new_deaths = int(state_wise_data_daily_new_deaths[-1])
    new_tests = int(state_wise_data_daily_tests[-1])

    change_in_24hr_cases = int(state_wise_data_daily_new_cases[-2] - state_wise_data_daily_new_cases[-3])
    per_change_in_24hr_cases = 100 * (state_wise_data_daily_new_cases[-2] - state_wise_data_daily_new_cases[-3]) / \
                               state_wise_data_daily_new_cases[-3]
    change_in_week_cases = int(state_wise_data_daily_new_cases[-2] - state_wise_data_daily_new_cases[-9])
    per_change_in_week_cases = 100 * (state_wise_data_daily_new_cases[-2] - state_wise_data_daily_new_cases[-9]) / \
                               state_wise_data_daily_new_cases[-9]
    change_in_month_cases = int(state_wise_data_daily_new_cases[-2] - state_wise_data_daily_new_cases[-32])
    per_change_in_month_cases = 100 * (state_wise_data_daily_new_cases[-2] - state_wise_data_daily_new_cases[-32]) / \
                                state_wise_data_daily_new_cases[-32]

    cases_yesterday = int(state_wise_data_daily_new_cases[-2])
    deaths_yesterday = int(state_wise_data_daily_new_deaths[-2])
    tests_yesterday = int(state_wise_data_daily_tests[-2])
    TPR_yesterday = round(100 * cases_yesterday / tests_yesterday, 2)
    TPR_Week = round(100 * state_wise_data_daily_new_cases[-8] / state_wise_data_daily_tests[-8], 2)
    TPR_Month = round(100 * state_wise_data_daily_new_cases[-31] / state_wise_data_daily_tests[-31], 2)
    datetime_last = pd.to_datetime(d1.iloc[-1:, :]['Date'].values)
    if curr_hour >= 16 and curr_date <= 23:
        delta_case = new_cases
        delta_deaths = new_deaths
        delta_tests = new_tests
    else:
        delta_case = cases_yesterday
        delta_deaths = deaths_yesterday
        delta_tests = tests_yesterday

    # print(datetime_last)
    date_last = datetime_last.day
    date_month = datetime_last.month
    date_year = datetime_last.year
    month_num = str(date_month[0])
    datetime_object = datetime.datetime.strptime(month_num, "%m")
    date_month = datetime_object.strftime("%b")
    # print("Short name: ",date_month)
    final_date = str(date_last[0]) + " " + str(date_month) + " " + str(date_year[0])
    # print(final_date)
    line1 = "Total COVID-19 Cases as of {} : {} (+ {} )".format(final_date, f"{tot_cases:,}", delta_case)
    line2 = "Total COVID-19 Related Deaths as of {} : {} (+ {} ) ".format(final_date, f"{tot_deaths:,}", delta_deaths)
    line0 = "Total Number of Samples Tested for COVID-19 as of {} : {} (+ {} ) ".format(final_date, f"{tot_tests:,}",
                                                                                        delta_tests)
    line3 = "NEW COVID-19 Cases Today: {}".format(f"{new_cases:,}")
    line4 = "NEW COVID-19 Deaths Today : {}".format(f"{new_deaths:,}")

    line5 = "COVID-19 Cases Yesterday: {}".format(f"{cases_yesterday:,}")
    line6 = "COVID-19 Deaths Yesterday: {}".format(f"{deaths_yesterday:,}")
    line13 = "Total Positivity Rate Yesterday: {}%".format(TPR_yesterday)

    line7 = "Increase/Decrease in Cases in last 24hrs: {}".format(f"{change_in_24hr_cases:,}")
    line8 = "Percentage Increase/Decrease in Cases in last 24hrs: {}%".format(round(per_change_in_24hr_cases, 2))

    line9 = "Increase/Decrease in A Week: {}".format(f"{change_in_week_cases:,}")
    line10 = "Percentage Increase/Decrease in a Week: {}%".format(round(per_change_in_week_cases, 2))
    line14 = "Total Positivity Rate Last Week: {}% ".format(TPR_Week)

    line11 = "Increase/Decrease in a Month: {}".format(f"{change_in_month_cases:,}")
    line12 = "Percentage Increase/Decrease in A Month: {}%".format(round(per_change_in_month_cases, 2))
    line15 = "Total Positivity Rate Last Month: {}% ".format(TPR_Month)

    df = pd.DataFrame()
    df['Date'] = d1['Date'][1:100]
    print(len(df))
    df['Date'] = pd.to_datetime(d1['Date'])
    df['Deaths'] = state_wise_data_daily_new_deaths[:-1]
    df['Number of COVID-19 Cases'] = state_wise_data_daily_new_cases[:-1]
    fig = px.bar(df, x='Date', y='Number of COVID-19 Cases', color='Deaths',
                 color_continuous_scale=px.colors.sequential.OrRd, hover_data={"Date": "|%d %B, %Y"},
                 title='Number of COVID-19 Cases and Deaths in {}'.format(input_state))
    fig.update_xaxes(dtick="M1", tickformat="%b\n%Y")
    # fig.show()

    graphJSON1 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    df = None
    fig = None

    # PLOT 2
    df = pd.DataFrame()
    df['Date'] = d1['Date'][1:100]
    df['Date'] = pd.to_datetime(d1['Date'])
    df['Number of Samples Tested'] = state_wise_data_daily_tests[:-1]
    df['TPR'] = state_wise_data_daily_tpr[:-1]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(x=df['Date'], y=df['Number of Samples Tested'], name="Daily Tests",
               hovertemplate='Date: %{x|%d, %b, %Y } <br> Tests: %{y:d}<extra></extra>'),
        secondary_y=False, )
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['TPR'], name="Positivity Rate (%)",
                   hovertemplate='Date: %{x|%d, %b, %Y} <br> %{y:.2f}%<extra></extra>'),
        secondary_y=True, )
    fig.update_layout(
        title_text="Daily COVID-19 Tests and Positivity Rate")
    fig.update_xaxes(title_text="Time")
    fig.update_xaxes(dtick="M1", tickformat="%b\n%Y")
    fig.update_yaxes(title_text="<b>Number of Samples Tested</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Positivity Rate</b>(in %)", secondary_y=True)
    graphJSON2 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


    head = input_state.upper()
    return render_template('home1.html',head=head,line1=line1,line2=line2,line3=line3,line4=line4,line5=line5,line6=line6,line7=line7,line8=line8,line9=line9,line10=line10,line11=line11,line12=line12,curr_datetime=curr_datetime,line0=line0,line13=line13,line14=line14,line15=line15,graphJSON1=graphJSON1,graphJSON2=graphJSON2)







if __name__ == "__main__":
    app.run(port=8000,debug=True) # running the app on the local machine on port 8000