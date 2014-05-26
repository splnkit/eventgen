'''
Copyright (C) 2005 - 2010 Splunk Inc. All Rights Reserved.
'''
import splunk.admin as admin
import splunk.entity as en

ENDPOINT = 'configs/conf-eventgen' 

required_args = ['outputMode']
optional_args = ['index']

class EventGenApp(admin.MConfigHandler):
    '''
    Set up supported arguments
    '''
    
    def setup(self):
        if self.requestedAction in [admin.ACTION_CREATE, admin.ACTION_EDIT]:
      
            for arg in required_args:
                self.supportedArgs.addReqArg(arg)

            for arg in optional_args:
                self.supportedArgs.addOptArg(arg)

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
                              
        for arg in required_args:
            ent[arg] = self.callerArgs[arg] 

        for arg in optional_args:
            try:
                ent[arg] = self.callerArgs[arg]
            except:
                pass

        en.setEntity(ent, sessionKey=self.getSessionKey())

    def handleCreate(self, confInfo):

        name = self.callerArgs.id
       
        new = en.Entity(ENDPOINT, name, 
                        namespace=self.appName, owner='nobody') 

        # new.properties['owner'] = 'nobody'
        # new.properties['sharing'] = 'global'

        # new[admin.EAI_ENTRY_ACL]['owner'] = 'nobody'
        # new[admin.EAI_ENTRY_ACL]['sharing'] = 'global'

        for arg in required_args:
            new[arg] = self.callerArgs[arg] 

        for arg in optional_args:
            try:
                new[arg] = self.callerArgs[arg]
            except:
                pass
        
        en.setEntity(new, sessionKey = self.getSessionKey())


    def handleRemove(self, confInfo):

        name = self.callerArgs.id

        en.deleteEntity(ENDPOINT, name,
                        namespace=self.appName,
                        owner=self.userName,
                        sessionKey = self.getSessionKey())

    # def handleList(self, confInfo):
    #     confDict = self.readConfCtx('eventgen')
    #     if confDict != None:
    #         for stanza, settings in confDict.items():
    #             for key, value in settings.items():
    #                 if key != 'eai:acl':
    #                     confInfo[stanza].append(key, str(value))
    #                 else:
    #                     confInfo[stanza].setMetadata(key, value)
                    
# initialize the handler
admin.init(EventGenApp, admin.CONTEXT_APP_AND_USER)