from flask import Flask

from flask_sqlalchemy import SQLAlchemy # for the ORM
from flask_restful import Api, Resource, request

import json # to read through the json file and add values to database

# initalizing the application
app = Flask(__name__)

# configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///htn.db'
db = SQLAlchemy(app) # create the database

from models import Applicant, Skills, Events # import the tables for the databse

# Class to add all the data from the given JSON into the database
class Data:
    def add_data(self):

        # opens and collects the data from the json, holds it as an array of dictionaries
        information = open('HTN_2023_BE_Challenge_Data.json')
        data = json.load(information)

        # itterate through the array of dictionaries
        for i in range (0, len(data)): 
            
            # the values of each field per contestant
            name_holder = data[i]["name"]
            company_holder = data[i]["company"]
            email_holder = data[i]["email"]
            phone_holder = data[i]["phone"]
            skills_holder = data[i]["skills"]
            events_holder = []

            # making the applicant in the database format
            applicant = Applicant(name=name_holder, email=email_holder, phone=phone_holder, company=company_holder, events=events_holder)
            
            db.session.add(applicant) # adding the applicant to the database

            # adding all the associated skills to the database
            for m in skills_holder:
                skill_name = m["skill"]
                skill_rating = m["rating"]
                skill_user_id = i + 1

                skill_item = Skills(skill=skill_name, rating=skill_rating, user_id=skill_user_id)
                db.session.add(skill_item)
            
            
            db.session.commit() # commit these additions to the database

# to initialize the database
with app.app_context():
   # db.drop_all()
    db.create_all()

   # Used to add all the data from the json into the database, only needed to be run once to create the database 
   # d = Data()
   # d.add_data()

# initialize REST API
api = Api(app)

# class used to get all the applicants and their information from the database
# Potential API requests:
# GET request: returns all users
class AllApplicants(Resource):
    # GET request: returns all users
    def get(self):
        applicants = Applicant.query.all()

        arr = [] # array to return with all the information from the database

        # for loop that runs through the length of the database, getting each applicant and their information
        for i in range (0, len(applicants)):
            # creating a dictionary to store all key,value pairs, and the skills array
            temp = dict()
            temp['name'] = applicants[i].name
            temp['email'] = applicants[i].email
            temp['phone'] = applicants[i].phone
            temp['company'] = applicants[i].company
            temp['skills'] = []
            temp['events'] = []

            # querying for all the skills that are corresponding to it's applicant
            skills = Skills.query.filter_by(user_id=applicants[i].id).all()
            # for loop to create the array of skills and ratiing
            for j in range (0, len(skills)):
                holder = dict()
                holder['skill'] = skills[j].skill
                holder['rating'] = skills[j].rating
                temp['skills'].append(holder)

            # querying for all the events that are corresponding to it's applicant
            events = Events.query.filter_by(user_id=applicants[i].id).all() # getting all their corresponding events
            # for loop to create the array of events
            for j in range (0, len(events)):
                holder = dict()
                holder['event'] = events[j].event
                holder['eType'] = events[j].eType
                temp['events'].append(holder)

            arr.append(temp) # adding the user to the array

        return arr # returning the database information on all the applicants in the JSON format


# class used to get a specific applicant and all their information
# Potential API requests:
# GET request: get a specific applicant and all their information
# PUT request: update/add information to an applicant's profile
class SpecificApplicant(Resource):
    # GET request: gets the specified user by name
    def get(self, name):

        applicant = Applicant.query.filter_by(name=name).first() # getting the desired applicant by name

        # checking if this is a valid applicant
        if not applicant:
            return {
                "message": "This is not a registered applicant"
            }
        
        applicant_id = applicant.id
        skills = Skills.query.filter_by(user_id=applicant_id).all() # getting all their corresponding skills
        
        skills_arr = [] # array to hold all their skills and associated ratings
        # populating 'skills_arr'
        for i in range (0, len(skills)):
            holder = dict()
            holder['skill'] = skills[i].skill
            holder['rating'] = skills[i].rating
            skills_arr.append(holder)
        
        events = Events.query.filter_by(user_id=applicant_id).all() # getting all their corresponding skills
        
        event_arr = [] # array to hold all their events attended
        # populating 'skills_arr'
        for i in range (0, len(events)):
            holder = dict()
            holder['event'] = events[i].event
            holder['eType'] = events[i].eType
            event_arr.append(holder)
        
        # the return value, holding all the specific applicant's information
        return {
            "name": applicant.name,
            "email": applicant.email,
            "phone": applicant.phone,
            "company": applicant.company,
            "skills": skills_arr,
            "events": event_arr

        }

    # PUT request: updates the fields of the specific user, cannot update field "events" as once they are scanned, no need to change it.
    def put(self, name):
        applicant = Applicant.query.filter_by(name=name).first() # gets the applicant

        # checking if this is a valid applicant
        if not applicant:
            return {
                "message": "This is not a registered applicant"
            }
        
        # checking if this is a valid input, specifically json format
        try:
            tester = request.json
        except:
            return {
                "message": "input must be in JSON format"
            }
        
        applicant_id = applicant.id # the applicant id
        skills = Skills.query.filter_by(user_id=applicant_id).all() # getting all their corresponding skills

        # if statements to see if the given json is updating certain fields, and if so, update these fields' values
        if 'name' in request.json:
            applicant.name = request.json['name']
        if 'email' in request.json:
            applicant.email = request.json['email']
        if 'phone' in request.json:
            applicant.phone = request.json['name']
        if 'company' in request.json:
            applicant.company = request.json['company']
        if 'skills' in request.json:
            
            # loop through all the given skills from the input
            for i in range (0, len(request.json['skills'])):
                holder_name = request.json['skills'][i]['skill'] # holds the skill's name
                new_skill_checker = True # boolean variable that is used to see if this is a new or existing skill being updated
                
                # itterate through current skills
                for j in range(0, len(skills)): 

                    # if this is a pre-existing skill, update the rating and set the 'new_skill_checker' variable to False; break out of loop
                    if holder_name == skills[j].skill: 
                        skills[j].rating = request.json['skills'][i]['rating']
                        new_skill_checker = False
                        break
                
                # if this is a new skill, make a 'Skills' object and add it to the database
                if new_skill_checker == True:
                    skill_name = holder_name
                    skill_rating = request.json['skills'][i]['rating']
                    skill_user_id = applicant_id

                    skill_item = Skills(skill=skill_name, rating=skill_rating, user_id=skill_user_id)
                    db.session.add(skill_item)
        
        db.session.commit() # commit the changes

        return self.get(applicant.name) # return all the information about the applicant
       

# class used to aggregate information about skills
# Potential API requests:
# GET request: get all the skills that have the frequency between the given minimum and maximum frequency
class SkillsAggregation(Resource):
    # GET request: gets the minimum and maximum frequency of a skill and returns all the skills within that range, inclusive with the bounds
    def get(self, min_freq, max_freq):
        skills = Skills.query.all() # getting all their corresponding skills
        dictionary_counter = dict() # dictionary to hold the count

        arr = [] # returning array to hold all the skills and their associated frequency

        # loop through all the skills and aggregate their frequencies
        for i in range(0, len(skills)):
            skill_name = skills[i].skill
            if skill_name in dictionary_counter: # if this skill already appeared, add 1 to the frequency
                dictionary_counter[skill_name] += 1
            else: # a new skill is found
                dictionary_counter[skill_name] = 1
        
        # loop through the dictionary and return all values that fit between the given minimum and maximum frequency
        for key, frequency in dictionary_counter.items():
            if min_freq <= frequency and frequency <= max_freq: # if this fits between the value, add this skill and associated frequency to the returning array
                holder = dict()
                holder['name'] = key
                holder['frequency'] = frequency
                arr.append(holder)
        
        return arr


# class that tracks an applicant's event participation
# Potential API requests:
# GET request: get all the events a user has participated in
# POST request: add an event to an applicant's profile ("scan" function)
class EventTracking(Resource):
    # GET request: gets all the events a specific person has been to
    def get (self, name):
        applicant = Applicant.query.filter_by(name=name).first() # gets the applicant
        
        # checking if this is a valid applicant
        if not applicant:
            return {
                "message": "This is not a registered applicant"
            }
        
        applicant_id = applicant.id # gets their id
        events = Events.query.filter_by(user_id=applicant_id).all() # gets all the events corresponding to the applicant

        arr = [] # will hold all the events

        # populate array with event information they have been to
        for i in range (0, len(events)):
            holder = dict()
            holder['event'] = events[i].event
            holder['eType'] = events[i].eType
            arr.append(holder)
        
        if not arr:
            return {
                "message": "this user has not attended any events yet!"
            }
        return arr
    
    # POST request: adds an event to the specific user
    def post (self, name):
        # gets the specific applicant
        applicant = Applicant.query.filter_by(name=name).first() # gets the applicant
        applicant_id = applicant.id

        # checking if this is a valid applicant
        if not applicant:
            return {
                "message": "This is not a registered applicant"
            }
                
        # checking if this is a valid input, specifically json format
        try:
            tester_event = request.json['event']
            tester_eType = request.json['eType']
        except:
            return {
                "message": "input must be in JSON format and contain the correct fields, 'event' and 'eType'"
            }

        events = Events.query.filter_by(user_id=applicant_id).all() # get the list events attended
        # checking to see if this event has already been added
        for i in range(0, len(events)):
            if request.json['event'] == events[i].event:
                return {
                    "message": "This event has already been scanned!"
                }

        # makes the specific event object and adds it to the database
        event_name = request.json['event']
        event_eType = request.json['eType']
        event_user_id = applicant_id
        event_item = Events(event=event_name,eType=event_eType,user_id=event_user_id)
        db.session.add(event_item)
        db.session.commit()

        # return all the information about the user through the get function of 'SpecificApplicant'
        s = SpecificApplicant() 
        return s.get(applicant.name)
        

# class to access information regarding the hackathon
# Potential API requests:
# GET request: get the information regarding the hackathon 
class HackerHelp(Resource):
    # GET reqiuest: displays information for hackers to view if curious about certain things (there should be more information, this is general to show a proof of concept)
    def get (self):
        string_description = "Feeling lost? Read this for more information and follow any links you see fit" # description of this page
        
        # getting help from mentors
        string_help = "If you need help, or maybe a push in the right direction to start Hacking, feel free to chat with one of our mentors!"
        mentors_arr = [{"name": "John Doe", "email": "john.doe@gmail.com"},
                        {"name": "Ezreal Dawn", "email": "ezredawn@uwaterloo.ca"},
                          {"name": "Ro Bot", "email": "robot@gmail.com"}, 
                          {"name": "Hack-the North", "email": "HTN@outlook.com"}]
        
        # prizes
        string_prizes = "Each category in this hackathon has their own prizes for the top 3 contestants! Follow this link to see our previous Hackathon's prizes (https://hackthenorth2022.devpost.com/)"

        # events
        events_arr = [{"name": "Starting off with Django", "type": "workshop"},
                       {"name": "Saturday night Starcraft!", "type": "activity"},
                         {"name": "meet n greet with Forbes 100 tech lords", "type": "event"}]

        # timefrme of hackathon
        timing_arr = [{"name": "introduction ceremony", "start time": "6:00pm EST Friday, February 24", "end time": "8:00pm EST Friday, February 24"},
                       {"name": "Hacking!", "start time": "8:00pm EST Friday, February 24", "end time": "11:00am EST Sunday, February 26"},
                         {"name": "Presenting to judges", "start time": "12:00pm EST Sunday, February 26", "end time": "4:00pm EST Sunday, February 26"},
                         {"name": "closing ceremonies", "start time": "6:00pm EST Sunday, February 26", "end time": "7:30pm EST Sunday, February 26"}]
        
        # end of page message
        ending_message = "Goodluck but more importantly, have fun! Enjoy this experience as much as we enjoyed making it for our participants!"
        
        # return value
        return {
            "description": string_description,
            "help": string_help,
            "mentors": mentors_arr,
            "prizes": string_prizes,
            "events": events_arr,
            "timeframe for Hack the North 2023": timing_arr,
            "exit message": ending_message
            
        }

# class for adding or removing an applicant:
# Potential API requests:
# POST request: add an applicant to the database
# DELETE request: remove an applicant from the database
class AddOrRemoveApplicant(Resource):
    # POST request: adds a user to the database
    def post(self):

        # error trapping to make sure the correct format of input was given
        try:
            tester = request.json
        except:
            return {
                "message": "The given input must be in JSON format"
            }
        
        # error trapping to see if the correct data was given
        try:     
            applicant_name = request.json['name']
            applicant_email = request.json['email']
            applicant_phone = request.json['phone']
            applicant_company = request.json['company']
        except:
            return {
                "message": "You must give the applicants name, email, phone and company. These are the required fields."
            }
        
        # adding this new applicant to the database
        applicant = Applicant(name=applicant_name,email=applicant_email,phone=applicant_phone,company=applicant_company)
        db.session.add(applicant)
        # the commit happens because we need to fetch this new applicant's user_id in order to link the
        # given skills and events to them, as done below  
        db.session.commit()

        # getting the applicant's user_id
        applicant_holder = Applicant.query.filter_by(name=applicant_name).first()
        applicant_id = applicant_holder.id

        # checking if there are any skills given
        given_skills = True
        try:
            applicant_skills = request.json['skills']
        except:
            given_skills = False
        
        # if there are given skills, add them to the database
        if given_skills == True:
            for m in applicant_skills:
                skill_name = m["skill"]
                skill_rating = m["rating"]
                skill_user_id = applicant_id

                skill_item = Skills(skill=skill_name, rating=skill_rating, user_id=skill_user_id)
                
                db.session.add(skill_item)

        # checking if there are any events given 
        given_events = True
        try:
            applicant_events = request.json['events']
        except:
            given_events = False
        
        # if there are given events, add them to the database
        if given_events == True:
            for m in applicant_events:
                event_name = m["event"]
                event_eType = m["eType"]
                event_user_id = applicant_id

                event_item = Events(event=event_name, eType=event_eType, user_id=event_user_id)
                
                db.session.add(event_item)
        
        db.session.commit() # add the new Events and Skills to the database

        # return all the information about the user through the get function of 'SpecificApplicant'
        s = SpecificApplicant() 
        return s.get(applicant.name)

    # DELETE request: deletes a user from the database
    def delete(self):

        # error trapping to make sure the correct format of input was given
        try:
            tester = request.json
        except:
            return {
                "message": "The given input must be in JSON format"
            }
        
        # error trapping to make sure the correct input is given
        try:
            applicant_id = request.json['user_id']
        except:
            return {
                "message": "You need to give the id of the applicant you want to delete"
            }
        
        applicant = Applicant.query.filter_by(id=applicant_id).first() # gets the applicant

        # error trapping so if there is no applicant with this id, return an according message
        if not applicant:
            return {
                "message": "there is not applicant with this user_id. Please enter a valid user_id"
            }
        
        db.session.delete(applicant) # delete the applicant from the database

        # delete all skills corresponding to the user
        while True:
            skills = Skills.query.filter_by(user_id=applicant_id).first()
            if not skills:
                break
            db.session.delete(skills)

        # delete all events corresponding to the user
        while True:
            events = Events.query.filter_by(user_id=applicant_id).first()
            if not events:
                break
            db.session.delete(events)

        db.session.commit() # commit these changes

        # return this message telling the user that this was successful
        return {
            "message": "this applicant has been deleted!"
        }


api.add_resource(AllApplicants, "/users/") # pathway for getting all applicants
api.add_resource(SpecificApplicant, "/users/<string:name>") # pathway for GET and PUT requests for specific users
api.add_resource(SkillsAggregation, "/skills/min=<int:min_freq> & max=<int:max_freq>") # pathway for GET request for aggregating skills
api.add_resource(EventTracking, "/events/<string:name>") # pathway for GET and POST requests for events related to users
api.add_resource(HackerHelp, "/information/") # pathway for GET request for information regarding the hackathon
api.add_resource(AddOrRemoveApplicant, "/addOrRemove/") # pathway for POST or DELETE request for adding/deleting applicants from the database