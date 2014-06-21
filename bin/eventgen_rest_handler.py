'''
Copyright (C) 2005 - 2010 Splunk Inc. All Rights Reserved.
'''
import splunk.admin as admin
import splunk.entity as en

ENDPOINT = 'configs/conf-eventgen' 

optional_args = ["disabled", "outputMode", "mode",
                 "sampletype", "index", "source",
                 "sourcetype", "host", "splunkPort",
                 "splunkMethod", "interval", "timeMultiple",
                 "count", "earliest", "latest",
                 "minuteOfHourRate", "hourOfDayRate",
                 "dayOfWeekRate", "randomizeCount",
                 "randomizeEvents", "timeField", "backfill",
                 "backfillSearch"]

class EventGenApp(admin.MConfigHandler):
    '''
    Set up supported arguments
    '''
    
    def setup(self):
        if self.requestedAction in [admin.ACTION_CREATE, admin.ACTION_EDIT]:

            for arg in optional_args:
                self.supportedArgs.addOptArg(arg)

            for i in xrange(len(self.callerArgs)):
                self.supportedArgs.addOptArg("token.%d.token" % i)
                self.supportedArgs.addOptArg("token.%d.replacementType" % i)
                self.supportedArgs.addOptArg("token.%d.replacement" % i)

    def handleList(self, confInfo):

        ent = en.getEntities(ENDPOINT,
                             namespace=self.appName,
                             owner=self.userName,
                             sessionKey=self.getSessionKey())

        for name, obj in ent.items():
            confItem = confInfo[name]
            for key, val in obj.items():
                confItem[key] = str(val)
            acl = {}
            for k, v in obj[admin.EAI_ENTRY_ACL].items():
                if None != v:
                    acl[k] = v
            confItem.setMetadata(admin.EAI_ENTRY_ACL, acl)

    def handleEdit(self, confInfo):

        name = self.callerArgs.id

        ent = en.getEntity(ENDPOINT, name,
                              namespace=self.appName,
                              owner=self.userName,
                              sessionKey=self.getSessionKey())

        for arg in self.callerArgs:
            if arg in optional_args or arg.startswith("token."):
                ent[arg] = self.callerArgs[arg]

        en.setEntity(ent, sessionKey=self.getSessionKey())


    def handleCreate(self, confInfo):

        name = self.callerArgs.id
       
        new = en.Entity(ENDPOINT, name, 
                        namespace=self.appName, owner='nobody') 

        for arg in self.callerArgs:
            if arg in optional_args or arg.startswith("token."):
                new[arg] = self.callerArgs[arg]
        
        en.setEntity(new, sessionKey = self.getSessionKey())


    def handleRemove(self, confInfo):

        name = self.callerArgs.id

        en.deleteEntity(ENDPOINT, name,
                        namespace=self.appName,
                        owner=self.userName,
                        sessionKey = self.getSessionKey())

# initialize the handler
admin.init(EventGenApp, admin.CONTEXT_APP_AND_USER)