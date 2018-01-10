from overrides import overrides
from MoonMachine.Models.DatedLabel import DatedLabel
from datetime import datetime

class BitbucketContext(object):
    """description of class"""

    def __init__(self):
        self.__CommitLabels = []
        self.__accessToken = str
        self.__refreshToken = str

    def TryAuthenticate(self, authCredentials = dict):
        authErrors = str

        try:
            pass

        except error:
            authErrors += ". " + "bitbucket" + ": " + error

        return authErrors
        

    def GetCommitLabels(self):
        if self.__CommitLabels.count() == 0:
            #return DatedLabel()
            pass

        else:
            return self.__CommitLabels.copy()