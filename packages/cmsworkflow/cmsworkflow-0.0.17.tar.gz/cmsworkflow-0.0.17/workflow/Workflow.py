"""
File       : Workflow.py
Author     : Hasan Ozturk <haozturk AT cern dot com>
Description: Workflow class provides all the information needed for the filtering of workflows in assistance manual.
"""

from workflow.utils.WebTools import getResponse
from workflow.utils.SearchTools import findKeys

from workflow.CacheableBase import CacheableBase,cached_json

import time
import traceback
import logging

class Workflow(CacheableBase):

    def __init__(self, workflowName, url='cmsweb.cern.ch'):
        """
        Initialize the Workflow class
        :param str workflowName: is the name of the workflow
        :param str url: is the url to fetch information from
        """
        super( Workflow , self).__init__()
        self.workflowName = workflowName
        self.url = url
        self.workflowParams = self.getWorkflowParams()
        self.requestType = self.workflowParams.get('RequestType')
        self.age = self.getAge()

        # N.B.: these should never be called directly
        # they are used to store the info, so that repetitive
        # calls to getErrors(), for example, can be sped up
        # FIXME: now that cache is working, we should remove this  fillX() and getX() thing,
        # since it's basically the same thing
        self._errors = None
        self._tasks = None
        self._jobStats = None

    def serialize(self):
        """
        the output of this method is used by the rest-api in the "AdditionalInfo" field
        """
        return { 
            'PrepID':self.getPrepID()
        }

    def __str__(self):
        return 'workflowinfo_%s' % self.workflowName
        
    @cached_json('workflow_params', timeout=48*3600)
    def getWorkflowParams(self):

        """
        Get the workflow parameters from ReqMgr2.
        See the `ReqMgr 2 wiki <https://github.com/dmwm/WMCore/wiki/reqmgr2-apis>`_
        for more details.
        :returns: Parameters for the workflow from ReqMgr2.
        :rtype: dict
        """

        try:
            result = getResponse(url=self.url,
                                 endpoint='/reqmgr2/data/request/',
                                 param=self.workflowName)

            if result is None:
                raise Exception("Failed to get response from reqmgr for {}. Double check the proxy validity.".format(self.workflowName))

            for params in result['result']:
                for key, item in list(params.items()):
                    if key == self.workflowName:
                        self.workflowParams = item
                        return item

        except Exception as error:
            logging.error(str(error))
            logging.error(traceback.format_exc())
            self.workflowParams = {}
            return {}

    def getTasksParams(self, getKey: str):

        """
        Get all tasks parameters from ReqMgr2.
        :returns: for each task, the getKey item in the workflowParams dictionary
        :rtype: dict
        """

        output = {}

        keys = self.workflowParams.keys()
        if 'Step1' in keys: identifier = 'Step'
        elif 'Task1' in keys: identifier = 'Task'
        elif 'ReReco' == self.requestType or 'ReReco' == self.workflowParams['OriginalRequestType']: identifier = False
        else:
            logging.error("No Steps or Tasks found in this workflow and the requestType is not ReReco. RequestType: " + str(self.requestType))
            return output

        # if MC
        if identifier:

            # WMagent-tasks
            for WM_agent_task in self.getTaskNames():

                # loop over all ReqMgr-tasks e.g. Step1, Step2, ...
                i = 1
                found = False
                while not found:
                    try:
                        ReqMgr_task = self.workflowParams[identifier+str(i)][identifier+'Name']
                        if ReqMgr_task in WM_agent_task.split("/")[-1]:
                            found = True 
                            key = self.workflowParams[identifier+str(i)][getKey]
                            output.update({WM_agent_task: key})
                        else: i+= 1
                    # reached the end
                    except KeyError:
                        break

        # if ReReco, there are no multiple tasks/steps
        else:
            key = self.workflowParams[getKey]
            # WMagent-tasks
            for WM_agent_task in self.getTaskNames(): output.update({WM_agent_task: key})

        return output

    def getPrepID(self):
        """
        :param: None
        :returns: PrepID
        :rtype: string
        """
        return self.workflowParams.get('PrepID')

    def filterTaskNames(self, tasks):
        """
        :param: list of tasks (strings)
        :returns: list of task names filtered.
        :rtype: list of str
        """

        filteredTasks = []
        for task in tasks:
            if any([v in task.lower() for v in ['logcollect','cleanup']]): continue
            filteredTasks.append(task)
        return filteredTasks

    def fillTaskNames(self):
        tasks = list(self.getErrors().keys())
        tasks = self.filterTaskNames(tasks)
        self._tasks = tasks

    def getTaskNames(self):
        """
        :param: None
        :returns: list of Tasks of the given workflow.
                  N.B.: these are not all the steps in a StepChain, these are all the tasks
                  for which error codes exist, i.e. in the WM agent json, used by getErrors,
                  they are the AgentJobInfo tasks.
        :rtype: list of str
        """
        if self._tasks is not None: 
            return self._tasks
        else:
            self.fillTaskNames()
            return self._tasks

    def getNumberOfEvents(self):
        """
        :param: None
        :returns: Number of events requested
        :rtype: int
        """
        return self.workflowParams.get('TotalInputEvents')

    def getRequestType(self):
        """
        :param: None
        :returns: Request Type
        :rtype: string
        """

        return self.workflowParams.get('RequestType')

    def getSiteWhitelist(self):
        """
        :param: None
        :returns: SiteWhitelist
        :rtype: string
        """

        return self.workflowParams.get('SiteWhitelist')

    def getCampaigns(self):
        """
        Function to get the list of campaigns that this workflow belongs to
        :param: None
        :returns: list of campaigns that this workflow belongs to
        :rtype: list of strings
        """

        return findKeys('Campaign', self.workflowParams)

    def getTasksCampaigns(self):
        """
        Function to get the campaign for each task
        :param: None
        :returns: dictionary with keys being task names, items being the campaigns
        :rtype: dict of strings
        """
        return self.getTasksParams('Campaign')

    ## Get runtime related values

    def getAge(self):
        """
        Number of days since the creation of the workflow
        :param: None
        :returns: Age of the workflow
        :rtype: float
        """
        try:
            if 'RequestTransition' not in self.workflowParams:
                return -1
            for transition in self.workflowParams['RequestTransition']:
                if transition['Status'] == 'assignment-approved':
                    return int(time.time()) - int(transition['UpdateTime'])
        except Exception as e:
            logging.error("Failed to get the age of workflow: The workflow has no assignment-approved history")
            logging.error(str(e))
            logging.error(traceback.format_exc())
            return -1

    def fillJobStats(self):

        try:
            response = getResponse(url=self.url,
                                   endpoint='/wmstatsserver/data/request/',
                                   param=self.workflowName)

            jobStatsPerTask = {}
            if not response['result']:
                raise Exception("Failed to get job stats from wmstatserver %s : response is None" % self.workflowName)

            for agentName, agentData in response['result'][0].get(self.workflowName)['AgentJobInfo'].items():
                for taskName, taskData in agentData['tasks'].items():
                    # Some tasks such as LogCollect, Cleanup etc. don't have job info
                    # TODO: Decide whether we should ignore such tasks or not. Ignore for now
                    if 'status' not in  taskData:
                        continue
                    else:
                        taskStatus = taskData['status']
                    nSuccess = taskStatus['success'] if 'success' in taskStatus else 0
                    nFailure = sum(taskStatus['failure'].values()) if 'failure' in taskStatus else 0
                    if taskName in jobStatsPerTask:
                        jobStatsPerTask[taskName]['nSuccess'] += nSuccess
                        jobStatsPerTask[taskName]['nFailure'] += nFailure
                    else:
                        jobStatsPerTask[taskName] = {'nSuccess': nSuccess, 'nFailure': nFailure}
            self._jobStats = jobStatsPerTask
        except Exception as e:
            logging.error(str(e))
            logging.error(traceback.format_exc())
            self._jobStats = {}

    def getJobStats(self):
        """
        :param None
        :returns: a dictionary containing number of successful and failed jobs for each task/step in the following format::
                  {<taskName>: 
                    nSuccess: X,
                    nFailure: Y
                  }
        :rtype: dict
        """
        if self._jobStats is not None: 
            return self._jobStats
        else:
            self.fillJobStats()
            return self._jobStats


    def getFailureRate(self):
        """
        :param None
        :returns: a dictionary containing failure rates for each task/step in the following format::
                  {task: failure_rate}
        :rtype: dict
        """

        try:
            failureRatePerTask = {}
            jobStats = self.getJobStats()
            for taskName, stats in jobStats.items():
                # Avoid division by zero, although we shouldn't have such data
                if stats['nFailure'] == 0 and stats['nSuccess'] == 0:
                    failureRatePerTask[taskName] = -1
                else:
                    failureRatePerTask[taskName] = stats['nFailure'] / (stats['nFailure'] + stats['nSuccess'])
            return failureRatePerTask
        except Exception as e:
            logging.error('Failed to get failure rate for %s ' % self.workflowName)
            logging.error(str(e))
            logging.error(traceback.format_exc())
            return {}
   

    ## Get request related values
    def getPrimaryDataset(self):
        """
        :assumption: every production workflow reads just one PD
        :param: None
        :returns: the name of the PD that this workflow reads
        :rtype: list
        """

        return findKeys('InputDataset', self.workflowParams)

    def getPrimaryDatasetLocation(self):
        """
        :assumption: every production workflow reads just one PD
        :param: None
        :returns: list of RSEs hosting the PD
        :rtype: list of strings
        """
        pass

    def getSecondaryDatasets(self):
        """
        :info: a workflow can read more than one secondary datasets
        :param: None
        :returns: list of the names of PUs that this workflow reads
        :rtype: list of strings
        """

        return findKeys('MCPileup', self.workflowParams)

    def getSecondaryDatasetsLocation(self):
        """
        :info: a workflow can read more than one secondary datasets
        :param: None
        :returns: dictionary containing PU name and location pairs
        :rtype: dict
        """
        pass

    def getPrimaryAAA(self):
        """
        Function to get the primaryAAA/TrustSitelists value of the request (Either True or False)
        :param: None
        :returns: the primaryAAA/TrustSitelists value of the request (Either True or False)
        :rtype: boolean
        """
        return self.workflowParams['TrustSitelists']

    def getSecondaryAAA(self):
        """
        Function to get the secondaryAAA/TrustPUSitelists value of the request (Either True or False)
        :param: None
        :returns: the secondaryAAA/TrustPUSitelists value of the request (Either True or False)
        :rtype: boolean
        """
        return self.workflowParams['TrustPUSitelists']

    # Write a unit test for this function
    def getReqMgrStatus(self):
        """
        :param None
        :returns: the ReqMgr status of the workflow
        :rtype: strings
        """
        return self.workflowParams["RequestStatus"]

    def getParentTaskName(self):
        """
        :param None
        :returns: the parent task. Parent task is the one for which the ACDC/recovery is created
        :rtype: Workflow object
        """
        if 'InitialTaskPath' in self.workflowParams:
            return self.workflowParams['InitialTaskPath']
        else:
            return None

    def getParentWorkflowName(self):
        """
        :param None
        :returns: the parent workflow. Parent workflow is the one for which the ACDC/recovery is created
        :rtype: Workflow object
        """
        if 'InitialTaskPath' in self.workflowParams:
            initialTaskPath = self.workflowParams['InitialTaskPath']
            parentWorkflowName = initialTaskPath.split('/')[1]
            return parentWorkflowName
        else:
            return None

    # Write a unit test for this function
    def isRecovery(self):
        """
        :param None
        :returns: True if the given workflow is a recovery workflow, False otherwise
                  Note that recovery workflows are different from regular ACDC workflows
        :rtype: bool
        """
        requestType = self.getRequestType()
        if requestType == 'Resubmission':
            if self.workflowParams['OriginalRequestType'] == 'ReReco':
                if 'ACDC' in self.workflowName:
                    return False
                else:
                    return True
            else:
                return False
        else:
            return False

    def fillErrors(self, getUnreported=True):

        try:

            result = getResponse(url=self.url,
                                 endpoint='/wmstatsserver/data/jobdetail/',
                                 param=self.workflowName)
            output = {}

            if not result or result['result'] == [{}]:
                raise Exception("Failed to get errors from wmstat server for {}: result is {}".format(self.workflowName, result))

            for stepName, stepData in result['result'][0].get(self.workflowName, {}).items():
                errors = {}
                for errorCode, errorCodeData in stepData.get('jobfailed', {}).items():
                    sites = {}
                    for site, siteData in errorCodeData.items():
                        if siteData['errorCount']:
                            sites[site] = siteData['errorCount']

                    if sites:
                        errors[errorCode] = sites

                if errors:
                    output[stepName] = errors

            if getUnreported:
                acdcServerResponse = getResponse(url=self.url,
                                                 endpoint='/couchdb/acdcserver/_design/ACDC/_view/byCollectionName',
                                                 param={'key': '"%s"' % self.workflowName, 'include_docs': 'true',
                                                        'reduce': 'false'})

                if 'rows' in acdcServerResponse:
                    for row in acdcServerResponse['rows']:
                        task = row['doc']['fileset_name']

                        newOutput = output.get(task, {})
                        newErrorCode = newOutput.get('-2', {})
                        modified = False
                        for fileReplica in row['doc']['files'].values():
                            for site in fileReplica['locations']:
                                modified = True
                                if site in newErrorCode:
                                    newErrorCode[site] += 1
                                else:
                                    newErrorCode[site] = 1

                        if modified:
                            newOutput['-2'] = newErrorCode
                            output[task] = newOutput

            # for step in list(output):
            #     if True in [(steptype in step) for steptype in ['LogCollect', 'Cleanup']]:
            #         output.pop(step)

            self._errors = output

        except Exception as e:
            logging.error('Failed to get errors for %s ' % self.workflowName)
            logging.error(str(e))
            logging.error(traceback.format_exc())
            self._errors = {}

    def getOutputDatasets(self):
        return self.workflowParams.get("OutputDatasets")
        
    def getTotalInputLumis(self):
        return self.workflowParams.get("TotalInputLumis")
        
    def getOutputLumis(self):
        output = {}
        for dataset in self.getOutputDatasets():
            dataset_info = getResponse(url=self.url, endpoint='/dbs/prod/global/DBSReader/filesummaries?dataset=', param=dataset)[0]
            lumi = dataset_info['num_lumi']
            output.update({dataset: lumi})
        return output

    def getPercentCompletions(self):
        output = {}
        for dataset, outputLumis in self.getOutputLumis().items():
            output.update({dataset: outputLumis/self.getTotalInputLumis()})
        return output

    @cached_json('workflow_errors')
    def getErrors(self, getUnreported=True):
        """
        Get the useful status information from a workflow
        :param bool getUnreported: Get the unreported errors from ACDC server
        :returns: a dictionary containing error codes in the following format::
              {step: {errorcode: {site: number_errors}}}
        :rtype: dict
        """
        if self._errors: 
            return self._errors        
        else: 
            self.fillErrors(getUnreported)
            return self._errors
