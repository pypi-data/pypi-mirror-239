import time
import os
import jira

JIRA_PAT_PATH = "/eos/cms/store/unified/restricted/cmsunified_creds/jira/jira.txt"

class JIRAClient:

    def __init__(self, debug=False,pat_path=JIRA_PAT_PATH,cookie=None):
        self.server='https://its.cern.ch/jira'
        self.pat = self.read_pat(pat_path)
        self.client = jira.JIRA('https://its.cern.ch/jira' , token_auth=self.pat)

    def read_pat(self, pat_path):
        with open(pat_path, 'r') as f:
            pat = f.read().strip()
        return pat

    def getTicketCreationTime(self, ticket):
        return ticket.fields.created

    def find(self, specifications):
        query = 'project=CMSCOMPPR'
        summary = specifications.get('prepID', specifications.get('summary', None))
        if summary:
            query += ' AND summary~"%s"' % summary

        if specifications.get('status', None):
            status = specifications['status']
            if status.startswith('!'):
                query += ' AND status != %s' % (status[1:])
            else:
                query += ' AND status = %s' % status

        if specifications.get('label', None):
            label = specifications['label']
            query += ' AND labels = %s' % label

        if specifications.get('text', None):
            string = specifications['text']
            query += ' AND text ~ "%s"' % string

        return self._find(query)

    def _find(self, query):
        return self.client.search_issues(query, maxResults=-1)
