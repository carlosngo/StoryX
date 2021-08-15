from django.conf import settings

from converter.models import Character, Prop, Entity
from converter.pipeline.spacy_util import SpacyUtil
from converter.pipeline.entity_extractor import EntityExtractor

import os
import csv
import math

columns = [
    {
        "name": "Action Line",
        "index": 2,
    },
    {
        "name": "Dialogue Content",
        "index": 3,
    },
    {
        "name": "Dialogue Speaker 1",
        "index": 4,
    },
    {
        "name": "Dialogue Speaker 2",
        "index": 5,
    },
    {
        "name": "Prop 1",
        "index": 6,
    },
    {
        "name": "Prop 2",
        "index": 7,
    },
    {
        "name": "Character 1",
        "index": 8,
    },
    {
        "name": "Character 2",
        "index": 9,
    },
]

def calculate_smc(x, y):
    m00 = 0
    m01 = 0
    m10 = 0
    m11 = 0
    print(x)
    print(y)
    for i in range(len(x)):
        if x[i] == 0 and y[i] == 0:
            m00 += 1
        elif x[i] == 0 and y[i] == 1:
            m01 += 1
        elif x[i] == 1 and y[i] == 0:
            m10 += 1
        elif x[i] == 1 and y[i] == 1:
            m11 +=1
    return (m00 + m11) / (m00 + m01 + m10 + m11)

def calculate_jc(x, y):
    m00 = 0
    m01 = 0
    m10 = 0
    m11 = 0
    for i in range(len(x)):
        if x[i] == 0 and y[i] == 0:
            m00 += 1
        elif x[i] == 0 and y[i] == 1:
            m01 += 1
        elif x[i] == 1 and y[i] == 0:
            m10 += 1
        elif x[i] == 1 and y[i] == 1:
            m11 +=1
    return m11 / (m01 + m10 + m11)

def calculate_cs(x, y):
    try:
        return calculate_dot_product(x, y) / (calculate_length(x) * calculate_length(y))
    except ZeroDivisionError:
        return 0

def calculate_dot_product(x, y):
    dot_product = 0
    for i in range(len(x)):
        dot_product += x[i] * y[i]
    return dot_product

def calculate_length(v):
    sum_of_squares = 0
    for i in range(len(v)):
        sum_of_squares += v[i] * v[i]
    return math.sqrt(sum_of_squares)

def read_csv_file(csv_file):
    rows = []
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        data = []
        for i in range(len(row)):
            data.append(row[i]) 
        rows.append(data)
    print(rows)
    result = {}
    for column in columns:
        responses_for_column = []
        csv_reader = csv.reader(csv_file, delimiter=',')
        for i in range(len(rows)):
            row = rows[i]
            responses_for_column.append(row[column["index"]])     
            result[column["name"]] = responses_for_column                   
    return result

def get_binary_representation(responses):
    result = {
        'story': {},
        'screenplay': {},
    }
    for column in columns:
        column_name = column['name']
        binary_representation = {}
        story_responses = responses['story'][column_name]
        story_result = []
        screenplay_responses = responses['screenplay'][column_name]
        screenplay_result = []
        current_binary = 1
        min_respondents = min(len(story_responses), len(screenplay_responses))
        for i in range(1, min_respondents):
            story_response = story_responses[i]
            screenplay_response = screenplay_responses[i]
            if story_response in binary_representation:
                story_result.append(binary_representation[story_response])
            else:
                story_result.append(current_binary)
                binary_representation[story_response] = current_binary
                current_binary -= 1
            
            if screenplay_response in binary_representation:
                screenplay_result.append(binary_representation[screenplay_response])
            else:
                screenplay_result.append(current_binary)
                binary_representation[screenplay_response] = current_binary
                current_binary -= 1

        story_result.sort()
        screenplay_result.sort()
        result['story'][column_name] = story_result
        result['screenplay'][column_name] = screenplay_result
        
    return result


class UnderstandingEvaluator:
    def evaluate_understanding(self):
        responses = {
            "dltk": {},
            "main": {},
        }
        dltk_story_responses_directory = settings.DLTK_STORY_RESPONSES_ROOT
        dltk_screenplay_responses_directory = settings.DLTK_SCREENPLAY_RESPONSES_ROOT
        main_story_responses_directory = settings.MAIN_STORY_RESPONSES_ROOT
        main_screenplay_responses_directory = settings.MAIN_SCREENPLAY_RESPONSES_ROOT
        
        for filename in os.listdir(dltk_story_responses_directory):
            responses['dltk'][filename] = {
                "story": {},
                "screenplay": {}
            }
            try:
                with open(os.path.join(dltk_story_responses_directory, filename)) as story_file:
                    responses['dltk'][filename]["story"] = read_csv_file(story_file)
                with open(os.path.join(dltk_screenplay_responses_directory, filename)) as screenplay_file:
                    responses['dltk'][filename]["screenplay"] = read_csv_file(screenplay_file)
            except FileNotFoundError:
                responses['dltk'].pop(filename)

        for filename in os.listdir(main_story_responses_directory):
            print(filename)
            responses['main'][filename] = {
                "story": {},
                "screenplay": {}
            }
            try:
                with open(os.path.join(main_story_responses_directory, filename)) as story_file:
                    responses['main'][filename]["story"] = read_csv_file(story_file)
                with open(os.path.join(main_screenplay_responses_directory, filename)) as screenplay_file:
                    responses['main'][filename]["screenplay"] = read_csv_file(screenplay_file)
            except FileNotFoundError:
                responses['main'].pop(filename)
        
        story_understanding = {
            "agg": {

            },
            "corpus": {
                "dltk": {
                    "stories": [],
                    "agg": {

                    }
                },
                "main": {
                    "stories": [],
                    "agg": {

                    }
                },
            }
        }
        for corpus in responses:

            for filename in responses[corpus]:
                binary_responses = get_binary_representation(responses[corpus][filename])
                story_responses = binary_responses['story']
                screenplay_responses = binary_responses["screenplay"]
                print('story_responses')
                print(story_responses)
                print('screenplay_responses')
                print(screenplay_responses)

                understanding = {
                    "elements": {},
                    "filename": filename, 
                }
                for column in columns:
                    column_name = column['name']
                    smc = calculate_smc(story_responses[column_name], screenplay_responses[column_name])
                    jc = calculate_jc(story_responses[column_name], screenplay_responses[column_name])
                    cs = calculate_cs(story_responses[column_name], screenplay_responses[column_name])
                    print(smc, jc, cs)
                    understanding['elements'][column_name] = {
                        "smc": smc,
                        "jc": jc,
                        "cs": cs,
                    }
                story_understanding['corpus'][corpus]['stories'].append(understanding)
        for corpus in story_understanding['corpus']:
            
            for column in columns:
                column_name = column['name']
                avg_smc = 0
                avg_jc = 0
                avg_cs = 0
                count = 0
                for i in range(len(story_understanding['corpus'][corpus]['stories'])):
                    avg_smc += story_understanding['corpus'][corpus]['stories'][i]['elements'][column_name]["smc"]
                    avg_jc += story_understanding['corpus'][corpus]['stories'][i]['elements'][column_name]["jc"]
                    avg_cs += story_understanding['corpus'][corpus]['stories'][i]['elements'][column_name]["cs"]
                    count += 1
                
                
                avg_smc /= count
                avg_jc /= count
                avg_cs /= count    
                story_understanding['corpus'][corpus]['agg'][column_name] = {
                    "avg_smc": avg_smc,
                    "avg_jc": avg_jc,
                    "avg_cs": avg_cs,
                }
            story_understanding['corpus'][corpus]['agg']["Dialogue Speaker (Average)"] = {
                "avg_smc": (story_understanding['corpus'][corpus]['agg']["Dialogue Speaker 2"]["avg_smc"] + story_understanding['corpus'][corpus]['agg']["Dialogue Speaker 1"]["avg_smc"]) / 2,
                "avg_jc": (story_understanding['corpus'][corpus]['agg']["Dialogue Speaker 2"]["avg_jc"] + story_understanding['corpus'][corpus]['agg']["Dialogue Speaker 1"]["avg_jc"]) / 2,
                "avg_cs": (story_understanding['corpus'][corpus]['agg']["Dialogue Speaker 2"]["avg_cs"] + story_understanding['corpus'][corpus]['agg']["Dialogue Speaker 1"]["avg_cs"]) / 2
            }
            story_understanding['corpus'][corpus]['agg']["Character (Average)"] = {
                "avg_smc": (story_understanding['corpus'][corpus]['agg']["Character 2"]["avg_smc"] + story_understanding['corpus'][corpus]['agg']["Character 1"]["avg_smc"]) / 2,
                "avg_jc": (story_understanding['corpus'][corpus]['agg']["Character 2"]["avg_jc"] + story_understanding['corpus'][corpus]['agg']["Character 1"]["avg_jc"]) / 2,
                "avg_cs": (story_understanding['corpus'][corpus]['agg']["Character 2"]["avg_cs"] + story_understanding['corpus'][corpus]['agg']["Character 1"]["avg_cs"]) / 2
            }
            story_understanding['corpus'][corpus]['agg']["Prop (Average)"] = {
                "avg_smc": (story_understanding['corpus'][corpus]['agg']["Prop 2"]["avg_smc"] + story_understanding['corpus'][corpus]['agg']["Prop 1"]["avg_smc"]) / 2,
                "avg_jc": (story_understanding['corpus'][corpus]['agg']["Prop 2"]["avg_jc"] + story_understanding['corpus'][corpus]['agg']["Prop 1"]["avg_jc"]) / 2,
                "avg_cs": (story_understanding['corpus'][corpus]['agg']["Prop 2"]["avg_cs"] + story_understanding['corpus'][corpus]['agg']["Prop 1"]["avg_cs"]) / 2
            }
            
        total = {
            "avg_smc": 0,
            "avg_jc": 0,
            "avg_cs": 0,
        }
        
        final_column_count = 0
        for column in story_understanding['corpus']['dltk']['agg']:
            story_understanding['agg'][column] = {
                "avg_smc": (story_understanding['corpus']['dltk']['agg'][column]["avg_smc"] + story_understanding['corpus']['main']['agg'][column]["avg_smc"]) / 2,
                "avg_jc": (story_understanding['corpus']['dltk']['agg'][column]["avg_jc"] + story_understanding['corpus']['main']['agg'][column]["avg_jc"]) / 2,
                "avg_cs": (story_understanding['corpus']['dltk']['agg'][column]["avg_cs"] + story_understanding['corpus']['main']['agg'][column]["avg_cs"]) / 2
            }
            total['avg_smc'] += story_understanding['agg'][column]["avg_smc"]
            total['avg_jc'] += story_understanding['agg'][column]["avg_jc"]
            total['avg_cs'] += story_understanding['agg'][column]["avg_cs"]
            final_column_count += 1
        
        for key in total:
            total[key] /= final_column_count
        
        

        story_understanding['total'] = total

        print(story_understanding['agg'])
        print(story_understanding['total'])
        return story_understanding