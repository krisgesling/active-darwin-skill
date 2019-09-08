import json
import csv

from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.parse import match_one


class ActiveDarwin(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.data_dir = self.root_dir + '/data/'
        self.playgrounds = self.load_csv('Playgrounds.csv')
        self.science_trail_points = self.load_json('science-trail-points.json')
        self.topics = [ p.get('name') for p in self.science_trail_points ]
        self.transport_types = ['scooter', 'bike', 'bus', 'taxi', 'carshare']

    def load_csv(self, csv_file):
        csv_file = self.data_dir + csv_file
        data = []
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            for idx, row in enumerate(reader):
                if idx == 0:
                    headers = row
                else:
                    obj = {}
                    for k, col in enumerate(row):
                        obj[headers[k]] = col
                    data.append(obj)

    def load_json(self, json_file):
        json_file = self.data_dir + json_file
        with open(json_file) as json_data:
            return json.load(json_data)['points']

    @intent_file_handler('tell.me.about.intent')
    def handle_tell_me_about(self, message):
        self.log.info(message.data.get('topic'))
        topic, conf = match_one(message.data.get('topic'), self.topics)
        point = [ p for p in self.science_trail_points if p['name'] == topic ]
        point = point[0]
        self.speak(point['snippet'])
        response = self.get_response(point['question'], num_retries=1)
        self.log.info('Submitting response for review')

    @intent_file_handler('where.is.transport.intent')
    def handle_where_is_transport(self, message):
        transport, conf = match_one(message.data.get('transport'), self.transport_types)
        self.speak_dialog('transport.closest', {'transport': transport})

    @intent_file_handler('darwin.events.intent')
    def handle_darwin_events(self, message):
        self.speak_dialog('darwin.events')

    @intent_file_handler('food.truck.intent')
    def handle_food_truck(self, message):
        self.speak_dialog('food.truck')

    @intent_file_handler('scooter.placement.intent')
    def handle_scooter_placement(self, message):
        self.speak_dialog('scooter.placement')

    @intent_file_handler('tree.down.intent')
    def handle_tree_down(self, message):
        self.speak_dialog('tree.down')

    @intent_file_handler('whats.fun.intent')
    def handle_whats_fun(self, message):
        response = self.get_response('wave.pool')
        self.speak_dialog('wave.pool.directions')

    @intent_file_handler('feedback.intent')
    def handle_feedback(self, message):
        response = self.get_response('feedback')
        response = self.get_response('favourite.thing')


def create_skill():
    return ActiveDarwin()
