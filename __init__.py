from mycroft                            import MycroftSkill, intent_handler
from mycroft.audio                      import wait_while_speaking
from mycroft.configuration.config       import LocalConf
from mycroft.configuration.locations    import USER_CONFIG
from mycroft.messagebus                 import Message
from pathlib                            import Path
import time
import fileinput
import os
import subprocess

class Language(MycroftSkill):
    def __init__(self):
        """
        Initialize the skill.
        """
        MycroftSkill.__init__(self)
        
    @intent_handler('change.language.intent')
    def change_language_intent(self, msg:Message):
        msg.data["language"] = self.get_response('which.language') 
        return self.change_language_to_intent(msg)
        
    @intent_handler('change.language.to.intent')
    def change_language_to_intent(self, msg:Message):
        try:
            lang = self.translate_namedvalues('language', ',')[msg.data["language"]]
        except:
            self.speak_dialog('thats.not.a.supported.language')
            return
        config = LocalConf(USER_CONFIG)
        if config["lang"].lower() == lang.lower():
            self.speak_dialog('language.already.set')
            return
        config["lang"] = lang
        self.speak_dialog('setting.language', {'language': {v: k for k, v in self.translate_namedvalues('language', ',').items()}[lang]})

        if lang.lower() == 'en-us':
            config["tts"]["marytts"]["lang"] = "en"
            config["tts"]["marytts"]["voice"] = "nanotts:en-US"
        elif lang.lower() == 'sv-se':
            config["tts"]["marytts"]["lang"] = "sv"
            config["tts"]["marytts"]["voice"] = "espeak:sv"
            
        with fileinput.FileInput(os.path.join(Path.home(), 'MagicMirror', 'config', 'config.js'), inplace=True) as f:
            for line in f:
                if 'let lang =' in line:
                    print(f'let lang = "{config["tts"]["marytts"]["lang"]}";')
                else:
                    print(line, end='')
        config.store()
        self.bus.emit(Message('configuration.updated'))
        wait_while_speaking()
        time.sleep(5)
        subprocess.Popen("pm2 restart MagicMirror".split(), stdout=subprocess.PIPE).communicate()     
        subprocess.Popen(f"bash {os.path.join(Path.home(), 'mycroft-core', 'start-mycroft.sh')} restart all".split(), stdout=subprocess.PIPE).communicate()
        
def create_skill() -> Language:
    return Language()
