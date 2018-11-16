import os, json, time
import random as rand

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
                raise TypeError('Associations were parsed in the wrong format.')
            self.associations = associations
        elif race == None:
            raise ValueError('If no associations are provided, a race type must be given.')
        elif race == 'Human':
            path = os.path.join('res', 'human_associations.json')
            with open(path, 'r') as json_file:
                self.associations = json.load(json_file)
        else:
            raise ValueError(race + ' is not a valid race type.')
        self.topics = []
        for root in self.associations:
            self.topics.append(root)
    def add_association(self, root, association):
        if root not in self.associations:
            self.associations[root] = []
        self.associations[root].append(association)
        if association not in self.associations:
            self.associations[association] = []
        self.associations[association] += [root, root]
        self.associations[association] += self.current_topics()
    def get_association(self, root):
        if root in self.associations and len(self.associations[root]) > 0:
            return rand.choice(self.associations[root])
        else:
            return None
    def get_topic(self, partners):
        topics = []
        for root in self.associations:
            for partner in partners:
                if root in partner.associations:
                    topics.append(root)
            if root in self.situation:
                topics.append(root)
            if root in self.interests:
                topics.append(root)
        topic = rand.choice(topics)
        return topic

class Conversation:
    def __init__(self, participants):
        self.topic = None
        self.participants = participants
        self.recent_topics = []
        self.current_speaker = None
    def start_conversation(self):
        pool = []
        for participant in self.participants:
            if participant.wants_to_converse:
                for i in range(participant.social):
                    pool.append(participant)
        ice_breaker = rand.choice(pool)
        self.current_speaker = ice_breaker
        self.topic = ice_breaker.get_topic(self.participants)
    def get_next_speaker(self):
        participants = []
        for participant in self.participants:
            if participant == self.current_speaker:
                continue
            elif participant.wants_to_converse:
                print('  %s wants to talk.' % (participant.name))
                if self.topic in participant.associations:
                    print('  %s knows about %s.' % (participant.name, self.topic))
                    participants += [participant] * participant.social
        if len(participants) < 1:
            print('The conversation has died down.')
            time.sleep(3)
            next_speaker = rand.choice(self.participants)
        else:
            next_speaker = rand.choice(participants)
        return next_speaker
    def converse(self):
        self.start_conversation()
        while True:
            print('%s starts talking about %s.' % (self.current_speaker.name, self.topic))
            wait_time = 5
            wait_time += rand.randrange(-3, 4)
            wait_time /= 2
            time.sleep(wait_time)
            print(self.current_speaker.name, 'stopped talking.')
            self.current_speaker = self.get_next_speaker()
            self.topic = self.current_speaker.get_association(self.topic)

if __name__ == '__main__':
    barry = ConversationTools('Barry', race='Human')
    fred = ConversationTools('Fred', race='Human')
    tim = ConversationTools('Tim', race='Human')
    conversation = Conversation([barry, fred, tim])
    conversation.converse()
