import os, json, time
import random as rand
from logger import Logger

RES_DIR = 'res'
LOG = True

if LOG:
    logger = Logger()

class ConversationEnd(Exception):
    def __init__(self):
        super().__init__(self)
        info = 'The conversation is dying down...'
        print(info)
        logger.log(info)


class ConversationTools:
    def __init__(self, name, associations=None, race=None):
        self.name = name
        partners = []
        self.wants_to_converse = True
        self.social = 1
        self.situation = []
        self.interests = []
        if associations != None:
            try:
                for root in associations:
                    for association in associations[root]:
                        break
                    break
            except TypeError:
                info = 'Associations were parsed in the wrong format.'
                raise TypeError(info)
                logger.log('Error: ' + info)
            self.associations = associations
        elif race == None:
            info = 'If no associations are provided, a race type must be given.'
            raise ValueError(info)
            logger.log('Error: ' + info)
        elif race == 'Human':
            path = os.path.join('res', 'human_associations.json')
            with open(path, 'r') as json_file:
                self.associations = json.load(json_file)
        else:
            raise ValueError(race + ' is not a valid race type.')
        self.topics = []
        for root in self.associations:
            self.topics.append(root)
    def add_association(self, root, association, reverse=True):
        if self.name not in [root, association]:
            if root not in self.associations:
                self.associations[root] = []
            self.associations[root].append(association)
            if reverse:
                if association not in self.associations:
                    self.associations[association] = []
                self.associations[association].append(root)
        info = '  %s now associates %s with %s.' % (self.name, association, root)
        logger.log(info)
        logger.save(self.name, self.associations)
    def get_association(self, root, recent_topics=None):
        if root not in self.associations:
            return None
        elif recent_topics != None:
            associations = [x for x in self.associations[root] if x not in recent_topics]
            if len(associations) < 1:
                raise ConversationEnd()
            association = rand.choice(associations)
        else:
            association = rand.choice(self.associations[root])
        return association
    def get_topic(self, listeners):
        topics = []
        for root in self.associations:
            topics.append(root)
            if root in self.situation:
                topics.append(root)
            if root in self.interests:
                topics.append(root)
        # for listener in [x.name for x in listeners if x.name in self.associations]:
        #     for topic in [x for x in topics if x in self.associations[listener]]:
        #         topics.append(topic)
        topic = rand.choice(topics)
        return topic

class Conversation:
    def __init__(self, participants):
        self.participants = participants
        self.speaker = None
        self.listeners = []
        self.topic = None
        self.recent_topics = []
    def start_conversation(self):
        pool = []
        for participant in self.participants:
            if participant.wants_to_converse:
                for i in range(participant.social):
                    pool.append(participant)
        speaker = rand.choice(pool)
        topic = speaker.get_topic(self.listeners)
        self.set_topic(speaker, topic)
    def progress_conversation(self):
        participants = []
        for listener in self.listeners:
            if listener.wants_to_converse:
                logger.log('    %s wants to talk.' % (listener.name))
                if self.topic in listener.associations:
                    logger.log('    %s knows about %s.' % (listener.name, self.topic))
                    participants += [listener] * listener.social
        if len(participants) > 0:
            self.pause(5)
            speaker = rand.choice(participants)
        else:
            raise ConversationEnd()
        topic = speaker.get_association(self.topic, self.recent_topics)
        logger.log('  %s associates %s with %s.' % (speaker.name, topic, self.topic))
        if topic == None:
            raise ConversationEnd()
        self.set_topic(speaker, topic)
    def converse(self):
        try:
            self.start_conversation()
            while True:
                info = '%s starts talking about %s.' % (self.speaker.name, self.topic)
                print(info)
                logger.log(info)
                for listener in self.listeners:
                    reverse = rand.choice([True] + [False] * 5)
                    if self.speaker.name not in listener.associations:
                        logger.log('    %s has just heard %s talk for the first time.' % (listener.name, self.speaker.name))
                        listener.add_association(self.speaker.name, self.topic, reverse=reverse)
                    elif self.topic not in listener.associations[self.speaker.name]:
                        logger.log('    %s has just heard %s talk about %s for the first time.' % (listener.name, self.speaker.name, self.topic))
                        listener.add_association(self.speaker.name, self.topic, reverse=reverse)
                self.pause(5)
                self.progress_conversation()
        except ConversationEnd:
            self.pause(10)
    def pause(self, pause_time):
        pause_time += rand.randrange(-3, 4)
        pause_time /= 5
        time.sleep(pause_time)
    def set_topic(self, speaker, topic):
        self.recent_topics.append(topic)
        if len(self.recent_topics) > 5:
            del self.recent_topics[0]
        self.speaker = speaker
        self.topic = topic
        self.listeners = [x for x in self.participants]
        self.listeners.remove(speaker)

if __name__ == '__main__':
    path = os.path.join(RES_DIR, 'male_names.json')
    with open(path, 'r') as json_file:
        male_names = json.load(json_file)
    path = os.path.join(RES_DIR, 'female_names.json')
    with open(path, 'r') as json_file:
        female_names = json.load(json_file)
    path = os.path.join(RES_DIR, 'last_names.json')
    with open(path, 'r') as json_file:
        last_names = json.load(json_file)
    genders = ['male', 'female']
    participants = []
    for i in range(10):
        gender = rand.choice(genders)
        if gender == 'male':
            name = rand.choice(male_names)
        else:
            name = rand.choice(female_names)
        name += ' %s' % (rand.choice(last_names))
        participants.append(ConversationTools(name, race='Human'))
    conversation = Conversation(participants)
    while True:
        conversation.converse()
