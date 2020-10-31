class StoryObj:
    def __init__(self, _phone_number, _audio_path):
        self.phone_number = _phone_number
        self.audio_path = _audio_path
        
    def get_number(self):
        return self.phone_number
    
    def get_path(self):
        return self.audio_path