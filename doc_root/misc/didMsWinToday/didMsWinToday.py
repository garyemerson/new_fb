#!/usr/bin/python3

import requests
from datetime import datetime, timedelta
from enum import Enum

Outcome = Enum('Outcome', 'InProgress, Scheduled, Win, Loss, NoGame, NotFound')

class Espn:
	endpoint = 'http://site.api.espn.com/apis/site/v2/sports/baseball/mlb/teams/'
	schedulepath = '/schedule'

	def getSchedule(self, teamId):
		getScheduleEndpoint = self.endpoint + str(teamId) + self.schedulepath
		return requests.get(getScheduleEndpoint, params={}).json()

class ScheduleParser:

	#targetEventDateTime is expected in PST
	def getEventByDate(self, scheduleJson, targetEventDateTime):
		for event in scheduleJson['events']:
			dateTimeOfEventString = event['date']
			dateTimeOfEvent = self.__getDateTimeFromString(dateTimeOfEventString)
			#print(str(dateTimeOfEvent))
			dateTimeOfEvent = dateTimeOfEvent - timedelta(hours=7)
			if targetEventDateTime.date() == dateTimeOfEvent.date():
				return event
			if targetEventDateTime.date() < dateTimeOfEvent.date():
				return None

	#dateString is expected in the format YYYY-MM-DDTHH:MMZ or 2020-07-29T15:34Z
	def __getDateTimeFromString(self, dateString):
		a = dateString.split("T")
		date = a[0]
		time = a[1]
		dateSplit = date.split("-")
		timeSplit = time.split("Z")[0].split(":")
		return datetime(int(dateSplit[0]), int(dateSplit[1]), int(dateSplit[2]), int(timeSplit[0]), int(timeSplit[1]))

	def getTeamOutcomeForEvent(self, eventJson, teamId):
		if eventJson == None:
			return Outcome.NoGame
		competition = eventJson['competitions'][0]
		eventStatus = competition['status']
		#print("event status found: " + str(eventStatus['type']['completed']))
		if eventStatus['type']['completed'] == False:
			if eventStatus['type']['description'] == 'In Progress':
				return Outcome.InProgress
			else:
				return Outcome.Scheduled
		#print('Status is marked as complete')

		for competitor in competition['competitors']:
			#print('Team found: ' + str(competitor['id']))
			if competitor['id'] == str(teamId):
				if competitor['winner'] == True:
					return Outcome.Win
				else:
					return Outcome.Loss

		#print('Team not found in event')
		return Outcome.NotFound

marinersStyleMap = {Outcome.Win:"font-size:56px; color:navy", Outcome.Loss:"font-size:42px; color:red", Outcome.InProgress:"font-size:36px; color:green", Outcome.Scheduled:"font-size:28px", Outcome.NoGame:"font-size:24px", Outcome.NotFound:"font-size:24px"}
marinersMessageMap = {Outcome.Win:"HELL FUCKIN YEAH THEY DID!!!", Outcome.Loss:"don't worry about it.", Outcome.InProgress:"Game is in progress... you should be watching it. wtf are you doing here?", Outcome.Scheduled:"Game is scheduled for later today. We'll see what happens.", Outcome.NoGame:"No game today. Check back tomorrow!", Outcome.NotFound:"Something went wrong. You should fix it."}
oriolesStyleMap = {Outcome.Win:"font-size:24px; color:orange", Outcome.Loss:"font-size:24px; color:red", Outcome.InProgress:"font-size:24px; color:green", Outcome.Scheduled:"font-size:24px", Outcome.NoGame:"font-size:24px", Outcome.NotFound:"font-size:24px"}
oriolesMessageMap = {Outcome.Win:"Yup, they did.", Outcome.Loss:"no LOL", Outcome.InProgress:"In progress!", Outcome.Scheduled:"Game is scheduled for later today, but who cares", Outcome.NoGame:"No game today, thank god.", Outcome.NotFound:"Something went wrong. You should fix it. Actually its the Orioles. Don't worry about it"}
giantsMessageMap = {Outcome.Win:"Unfortunately yeah.", Outcome.Loss:"HELL NO LOL", Outcome.InProgress:"In progress... of losing", Outcome.Scheduled:"Game is scheduled for later today, so prob not", Outcome.NoGame:"No game today.", Outcome.NotFound:"Something went wrong. You should fix it. Actually its the Giants. Don't worry about it"}
styleMaps = {12:marinersStyleMap, 1:oriolesStyleMap, 26:oriolesStyleMap}
messageMaps = {12:marinersMessageMap, 1:oriolesMessageMap, 26:giantsMessageMap}

#Mariners = 12, Orioles = 1, Giants = 26
teamIds = [12, 1, 26]
espn = Espn()
parser = ScheduleParser()
#Determine today's date. Assumes system time is in UTC
pstDateTime = datetime.now() - timedelta(hours=7)
htmlStringFormat = "<p style=font-size:36px>Did the {} win today?</p><p style=\"{}\">{}</p>"
htmlString = ""
for teamId in teamIds:
	#Retrieve team Schedule from espn api https://gist.github.com/akeaswaran/b48b02f1c94f873c6655e7129910fc3b
	teamSchedule = espn.getSchedule(teamId)
	teamName = teamSchedule['team']['displayName']
	targetEvent = parser.getEventByDate(teamSchedule, pstDateTime)
	outcome = parser.getTeamOutcomeForEvent(targetEvent, teamId)
	htmlString += htmlStringFormat.format(teamName, styleMaps[teamId][outcome], messageMaps[teamId][outcome])
print(htmlString)
