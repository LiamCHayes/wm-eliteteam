### Modules for progress tracker

## Setup
from ast import Index
import csv
from itertools import islice
from datetime import datetime
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import random

def check_member(splitdata, fieldnames):
    # Check if name is on the team, if not then add to team and create personal CSV file
    # Returns id number of team member
    while True:
        with open('data/teammembers.csv', 'rt') as f:
            reader = csv.reader(f)
            for row in reader:
                team_member = row[1] == splitdata[0]
                id_num = row[0]
                if team_member:
                    break

        #create csv file if not team member and add to roster. Also can respell name if misspelled
        if not team_member:
            print('\n[ERROR]: ', splitdata[0], ' is not on the team. Would you like to make a data file for ', splitdata[0], ' and add them to the team?\nType respell to respell.')
            add_member = input('(add/respell/quit)>')
            if add_member.capitalize() == 'Add':
                with open(('data/' + splitdata[0] + '.csv'), 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(fieldnames)
                with open('data/teammembers.csv', 'r') as f:
                    reader = csv.reader(f)
                    for row in islice(reader, 1, None):
                        num_members = int(float(row[0])) + 1
                with open('data/teammembers.csv', 'a', newline='') as f:
                    writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([num_members, splitdata[0]])
                id_num = num_members
                break
            elif add_member.capitalize() == 'Respell':
                splitdata[0] = input('Name: ').capitalize()
            else:
                break
        else:
            break
    return id_num

class teamtracker:
    def __init__(self):
        self.benchmark_fields = ['Date', 'ID', 'Name', '35mm_hang', '20mm_hang', '15mm_hang', '10mm_hang', 'Jug_1arm_hang', 'Bmmedge_1arm_hang']
        self.field_names = ['Date', 'ID', 'Name', 'Grade', 'Flash', 'Zone', 'Lift', 'Weight', 'Reps']
        self.newdata = []

    def getinput(self):
        # Gets prompt for program
        self.newdata = input('\n\nName     Lift    Weight            Reps\nName     Grade   Flash(T/F)        Zone\nLookup   Name    Climb/Lift/Goal\n\nBenchmark to input a benchmark\nGroup to make groups\nQuit to quit\n............\n>')
        return self.newdata

    def benchmark(self): # NEEDS TO BE FINISHED (line 79, 88, 92. Also add function to catch misspelling, add member to team from benchmark screen)
        # Get benchmark data and write to benchmark.csv
        print('\nBenchmark Types: ', self.benchmark_fields)
        bench_data = input('Name Benchmark_type Benchmark_value\n>')

        #split input to add to CSV
        splitdata = bench_data.split()
        i = 0
        for j in splitdata:
            splitdata[i] = j.capitalize()
            i+=1

        #parse fields to get correct benchmark type
        while True:
            bench_id = 0
            for k in self.benchmark_fields:
                btype = splitdata[1] == k
                if btype:
                    benchmark_type = k
                    break
                else:
                    bench_id += 1
                    btype = False
            
            if not btype:
                print('[ERROR]: ', splitdata[1], ' is not a current benchmark type. Would you like to add it? Type respell to respell')
                add_benchmark = input('(add/respell/quit)>')
                if add_benchmark.capitalize() == 'Add':
                    # add a column to the csv file here
                    break
                elif add_benchmark.capitalize() == 'Respell':
                    splitdata[1] = input('Benchmark type: ').capitalize()
                else:
                    break
            else:
                break

        #standardize benchmark data to input 
        now = datetime.now()
        dt_string = now.strftime('%d/%m/%Y')
        date = dt_string

        bench_row = [None] * (len(self.benchmark_fields) + 1)
        bench_row[0] = date
        #bench_row[1] = 
        bench_row[2] = splitdata[0]
        bench_row[bench_id] = splitdata[2]

        with open('data/benchmarks.csv', 'a', newline='') as f:
            writer = csv.writer(f,  delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(bench_row)

    def input_data(self):
        # Write data to CSV
        #split input to add to CSV
        splitdata = self.newdata.split()
        i = 0
        for j in splitdata:
            splitdata[i] = j.capitalize()
            i+=1

        #check if member is on team and get id number of member
        id_num = check_member(splitdata, self.field_names)

        #if we are inputting a climb, set lift, weight, and reps to None
        if splitdata[1][0] == 'V':
            lift, weight, reps = None, None, None
            name, grade, flash, zone = splitdata[0], splitdata[1], splitdata[2], splitdata[3]
        #if we are inputting a list, set grade, flash, and zone to None
        else: 
            grade, flash, zone = None, None, None
            name, lift, weight, reps = splitdata[0], splitdata[1], splitdata[2], splitdata[3]

        #add the data to their csv file
        now = datetime.now()
        dt_string = now.strftime('%d/%m/%Y')
        date = dt_string
        dictionary = {self.field_names[0]: date, self.field_names[1]: id_num, self.field_names[2]: name, 
                        self.field_names[3]: grade, self.field_names[4]: flash, self.field_names[5]: zone, 
                        self.field_names[6]:lift, self.field_names[7]: weight, self.field_names[8]: reps}
        with open('data/' + splitdata[0] + '.csv', 'a', newline='') as f:
            dict_obj = csv.DictWriter(f, fieldnames=self.field_names)
            dict_obj.writerow(dictionary)

    def get_data(self):
        # Allows user to query files to get team member's progress for climbs and lifts
        splitdata = self.newdata.split()
        i = 0
        for j in splitdata:
            splitdata[i] = j.capitalize()
            i+=1

        filename = 'data/' + splitdata[1] + '.csv'
        if splitdata[2] == 'Climb':
            # get data and clean for output
            stats = pd.read_csv(filename, usecols=['Grade', 'Flash', 'Zone', 'Date'])
            stats = stats.dropna(axis=0, subset=['Grade'])
            datelist = pd.to_datetime(stats.loc[:, 'Date'], format='%d/%m/%Y')
            i=0
            for j in datelist:
                print(type(j))
                datelist[i] = j.strftime('%m/%d/%Y')
                print(i, datelist[i], j.strftime('%m/%d/%Y'))
                i += 1
            stats = stats[['Grade', 'Flash', 'Zone']]
            stats = pd.concat([stats, datelist], axis=1)
            stats = stats.dropna(axis=0, subset=['Grade'])
            grade = stats.loc[:,'Grade']
            gradenum = [None] * grade.size
            i=0
            for j in grade:
                gradenum[i] = j[1]
                i+=1
            stats_disp = stats.iloc[-3:]
            df_string = stats_disp.to_string(header=False, index=False, index_names=False).split()
            df_string = [' '.join(ele.split()) for ele in df_string]
            print(df_string)

            # output
            if df_string[0] != 'Empty':
                # find best flash and send
                flashes = list()
                sends = list()
                i=0
                for f in stats.loc[:, 'Flash']:
                    if f == 'T':
                        flashes.append(i)
                    else:
                        sends.append(i)
                    i+=1

                # output some data to terminal
                print('\n\n\tMost recent sends: \n')
                print('\t Date         Grade  Flash   Zone')
                i=0
                while i < len(df_string):
                    print('\t', df_string[i+3], ' ', df_string[i], '   ', df_string[i+1], '     ', df_string[i+2])
                    i+=4
                if sends != []:
                    bestsend = max(stats.iloc[sends, 0])
                    print('\n\tBest recorded send is', bestsend)
                else:
                    print('\n\t*No sends recorded yet*')
                if flashes != []:
                    bestflash = max(stats.iloc[flashes, 0])
                    print('\tBest recorded flash is', bestflash)
                else:
                    print('\t*No flashes recorded yet*')

                # create visualizations. mosaic of completions by zone, histogram of flashes/sends by zone
                # breakdown by zone
                fig, axs = plt.subplots(1, 4, figsize=(12,6), sharey=False)
                fig.tight_layout()
                fig.subplots_adjust(bottom=0.15)
                # Zone breakdown
                zone_freq = stats['Zone'].value_counts()
                axs[0].bar(zone_freq.keys(), zone_freq.astype(int), alpha=0.4)
                axs[0].set_title('Total', fontweight='bold')
                axs[0].tick_params(axis='both', which='both', bottom=False, top=False, left=False, labelbottom=True)
                # histogram
                flash_freq = stats[(stats['Flash'] == 'T')]
                send_freq = stats[(stats['Flash'] == 'F')]
                zonef_freq = flash_freq['Zone'].value_counts()
                zones_freq = send_freq['Zone'].value_counts()
                #flashes
                axs[1].bar(zonef_freq.keys(), zonef_freq.astype(int), alpha=0.4)
                axs[1].set_title('Flashes', fontweight='bold')
                axs[1].tick_params(axis='both', which='both', bottom=False, top=False, left=False, labelbottom=True)
                #sends
                axs[2].bar(zones_freq.keys(), zones_freq.astype(int), alpha=0.4)
                axs[2].set_title('Not Flashes', fontweight='bold')
                axs[2].tick_params(axis='both', which='both', bottom=False, top=False, left=False, labelbottom=True)
                #progress
                axs[3].plot(stats['Date'], stats['Grade'], alpha=.7)
                axs[3].set_title('Progress', fontweight='bold')
                axs[3].tick_params(axis='both', which='both', bottom=False, top=False, left=False, labelbottom=False)
                #formatting for all plots
                label_format = '{:,.0f}'
                for i in range(len(axs)):
                    axs[i].set_xlabel('')
                    axs[i].set_ylabel('')
                    axs[i].set_yticklabels([])
                    axs[i].tick_params(axis='x', labelrotation = 80)
                    axs[i].locator_params(axis='y', integer=True, tight=True)
                    warnings.filterwarnings('ignore')
                sns.despine(fig=fig, left=True, bottom=True)

                # close all plots
                plt.waitforbuttonpress(0)
                plt.close('all')

            # if there's enough data, line plot of progress(color coded to flash)
        elif splitdata[2] == 'Goal':
            # Return responses to goal questions
            pass
        else:
            # get data and clean for output
            stats = pd.read_csv(filename, usecols=['Lift', 'Weight', 'Reps', 'Date'])
            stats = stats.dropna(axis=0, subset=['Lift'])
            datelist = pd.to_datetime(stats.loc[:, 'Date'], format='%d/%m/%Y')
            stats = stats[['Lift', 'Weight', 'Reps']]
            stats_date = pd.concat([stats, datelist], axis=1)
            recent_date = max(datelist)
            recent_date = recent_date.strftime('%m/%d/%Y')

            # return last day of lifting performance and max weight
            weight = stats.loc[:, 'Weight']
            # give last day for exercise that is NOT today
            if max(datelist) == pd.Timestamp(date.today()):
                stats_date0 = stats_date[stats_date.Date != pd.Timestamp(date.today())]
                stats_date0 = stats_date0[(stats_date0['Date'] == max(pd.Series(stats_date0['Date'])))]
                recent_date = max(stats_date0['Date'])
                recent_date = recent_date.strftime('%m/%d/%Y')
                df_string = stats_date0.to_string(header=False, index=False, index_names=False).split()
                df_string = [' '.join(ele.split()) for ele in df_string]
            else:
                stats_date = stats_date[(stats_date['Date'] == max(datelist))]
                df_string = stats_date.to_string(header=False, index=False, index_names=False).split()
                df_string = [' '.join(ele.split()) for ele in df_string]
            # find max weight for how many reps
            maxes = list()
            i=0
            for m in weight:
                if m == max(weight):
                    maxes.append(i)
                i+=1
            max_reps = max(stats.iloc[maxes, 2])

            # output
            if df_string[0] != 'Empty':
                print('\n\n\tLast', splitdata[2], 'day was on', recent_date, ':\n')
                print('\t Weight   Reps')
                i=0
                while i < len(df_string):
                    print('\t', df_string[i+1],'   ', df_string[i+2])
                    i+=4
                print('\n\tMax recorded weight is', max(weight), 'lbs for', max_reps, 'reps')
        # wait for keypress to continue
        input('\n\nPress enter...')
            
    def groups(self):
        group_num = int(input('\nNumber of groups: '))
        names = input('Names of members here (space separated): ')
        splitdata = names.split()
        i = 0
        for j in splitdata:
            splitdata[i] = j.capitalize()
            i+=1
        group_size = int(len(splitdata)/group_num)

        def chunks(l, n):
            """Yield successive n-sized chunks from l."""
            for i in range(0, len(l), n):
                yield l[i:i + n]

        random.shuffle(splitdata)
        teams = list(chunks(splitdata, int(group_size)))

        print('\n')
        if (len(splitdata) % group_num) == 0:
            i=1
            for j in teams:
                print('\n\tTeam ' + str(i) + ':', j)                  
                i+=1
        elif (len(splitdata) % group_num) == 1:
            teams[0].append(teams[group_num][0])
            teams.remove(teams[group_num])
            i=1
            for j in teams:
                print('\n\tTeam ' + str(i) + ':', j)                  
                i+=1
        elif (len(splitdata) % group_num) == 2:
            teams[0].append(teams[group_num][0])
            teams[1].append(teams[group_num][1])
            teams.remove(teams[group_num])
            i=1
            for j in teams:
                print('\n\tTeam ' + str(i) + ':', j)                  
                i+=1
        else:
            i=1
            for j in teams:
                if i > group_num:
                    print('\n\tExtra:', j) 
                else:   
                    print('\n\tTeam ' + str(i) + ':', j)        
                i+=1

        # wait for keypress to continue
        input('\n\nPress enter...')


        

