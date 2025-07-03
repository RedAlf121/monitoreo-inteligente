import importlib


def send(message_type:str,**kwargs):
    url = 'services.messager.'+message_type+'.views'
    module = importlib.import_module(url)
    module.send(**kwargs)