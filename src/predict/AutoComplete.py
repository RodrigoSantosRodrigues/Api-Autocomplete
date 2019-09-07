# -*- coding: utf-8 -*-
#src/predict/AutoComplete.py
"""
                     Api Auto complete
    ------------------------------------------------------------------------
                        Lib | Predict | Auto Complete
    ------------------------------------------------------------------------
    
    URLs: https://flask.palletsprojects.com/en/1.1.x/
 
    
    
"""
from quart import g
import autocomplete
from autocomplete import models
from ..models.CollectorModel import CollectorModel, CollectorSchema

collector_schema = CollectorSchema()

class Complete():
    
    @staticmethod
    async def completing(letters):
        """
            predict_currword() 
        """
        text= ' '
        words= await Complete.fetch_all_saved_user_events()
        for i in range(0, len(words)):
            pos= words[i]
            text= text+' '+str(pos['event'])

        models.train_models(text)
        return autocomplete.predict_currword(letters)



    async def fetch_all_saved_user_events():
        """

        """
        events = await CollectorModel.get_event_by_user(g.user.get('id'))
        data = collector_schema.dump(events, many=True).data
        return data