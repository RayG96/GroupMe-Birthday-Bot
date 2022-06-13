import requests
import csv
import json
from datetime import datetime
from dateutil.parser import parse
from dotenv import load_dotenv
import random
import os

load_dotenv()

firstNameCol = 1
lastNameCol = 0
dateOfBirthCol = 2
groupMeIDCol = 3
botID = os.environ.get("botID")

emojis = ['\U0001F382', '\U0001F973', '\U0001F389', '\U0001F388', '\U0001F38A']
happyBirthdayMessage = 'Happy Birthday ' + emojis[random.randint(0, len(emojis) - 1)]

with open('Roster.csv') as csv_file:
    lineCount = 0
    birthdays = []
    csv_reader = csv.reader(csv_file, delimiter = ',')
    for row in csv_reader:
        if lineCount > 0:
            try:
                date = parse(row[dateOfBirthCol])
                # print(f'{row[firstNameCol]} {row[lastNameCol]}, {date.date()}, {date.replace(year = 1).date() == datetime.today().replace(year = 1).date()}')
                if date.replace(year = 1).date() == datetime.today().replace(year = 1).date():
                    print(f'{row[firstNameCol]} {row[lastNameCol]}, {date.date()}, {date.replace(year = 1).date() == datetime.today().replace(year = 1).date()}')
                    birthdays.append({'name': f'{row[firstNameCol]} {row[lastNameCol]}', 'id': row[groupMeIDCol]})
            except:
                print(f'Error occured at line {lineCount}')
        lineCount += 1
    if len(birthdays) == 1:
        mentionStartingIndex = len(happyBirthdayMessage) + 2
        mentionNumCharacters = len(birthdays[0]['name'])
        obj = {'bot_id': botID, 'text': f"{happyBirthdayMessage} {birthdays[0]['name']}!!", 'attachments': [{'loci': [[mentionStartingIndex, mentionNumCharacters]], 'type': 'mentions', 'user_ids': [birthdays[0]['id']]}]}
    elif len(birthdays) == 2:
        mentionStartingIndexFor1 = len(happyBirthdayMessage) + 2
        mentionNumCharactersFor1 = len(birthdays[0]['name'])
        mentionStartingIndexFor2 = mentionStartingIndexFor1 + len(birthdays[0]['name']) + 5
        mentionNumCharactersFor2 = len(birthdays[1]['name'])
        obj = {'bot_id': botID, 'text': f"{happyBirthdayMessage} {birthdays[0]['name']} and {birthdays[1]['name']}!!", 'attachments': [{'loci': [[mentionStartingIndexFor1, mentionNumCharactersFor1], [mentionStartingIndexFor2, mentionNumCharactersFor2]], 'type': 'mentions', 'user_ids': [birthdays[0]['id'], birthdays[1]['id']]}]}
    elif len(birthdays) > 2:
        message = happyBirthdayMessage + ' '
        loci = []
        userIDs = []
        mentionStartingIndex = len(happyBirthdayMessage) + 2
        mentionNumCharacters = len(birthdays[0]['name'])
        for index in range(0, len(birthdays) - 1):
            message += birthdays[index]['name'] + ', '
            loci.append([mentionStartingIndex, mentionNumCharacters])
            userIDs.append(birthdays[index]['id'])
            mentionStartingIndex += mentionNumCharacters + 2
            mentionNumCharacters = len(birthdays[index + 1]['name'])
        mentionStartingIndex += 4
        message += 'and ' + birthdays[len(birthdays) - 1]['name']
        loci.append([mentionStartingIndex, mentionNumCharacters])
        userIDs.append(birthdays[len(birthdays) - 1]['id'])
        obj = {'bot_id': botID, 'text': message + "!!", 'attachments': [{'loci': loci, 'type': 'mentions', 'user_ids': userIDs}]}
    if len(birthdays) > 0:
        url = "https://api.groupme.com/v3/bots/post"
        response = requests.post(url, json=obj)
        print(response.status_code)
    else:
        print("No birthdays today", datetime.now()