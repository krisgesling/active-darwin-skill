from mycroft import MycroftSkill, intent_file_handler


class ActiveDarwin(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('darwin.active.intent')
    def handle_darwin_active(self, message):
        self.speak_dialog('darwin.active')


def create_skill():
    return ActiveDarwin()

