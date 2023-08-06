#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2012-2014 Luiko Czub, TestLink-API-Python-client developers
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# ------------------------------------------------------------------------

# this test requires an online TestLink Server, which connection parameters
# are defined in environment variables
#     TESTLINK_API_PYTHON_DEVKEY and TESTLINK_API_PYTHON_DEVKEY
#
# works with the example project NEW_PROJECT_API  (see TestLinkExample.py)
# FIME LC 29.10.29: test does not really interacts with test link
#                   only negative test with none existing IDs implemented
#                   ok to check every implemented server call one time but not
#                   to cover all possible responses or argument combinations

import sys
import os.path

if sys.version_info[0] == 2 and sys.version_info[1] == 6:
    # py26 needs backport unittest2
    import unittest2 as unittest
else:
    import unittest
    
if sys.version_info[0] == 2 and sys.version_info[1] == 7:
    # py27 and py31 assertRaisesRegexp was renamed in py32 to assertRaisesRegex
    unittest.TestCase.assertRaisesRegex = unittest.TestCase.assertRaisesRegexp
    # py27 and py31 assertRegexpMatches was renamed in py32 to assertRegex
    unittest.TestCase.assertRegex = unittest.TestCase.assertRegexpMatches


from testlink import TestlinkAPIClient, TestLinkHelper
from testlink.testlinkerrors import TLResponseError

# example text file attachment = this python file
# why not using os.path.realpath(__file__)
# -> cause __file__ could be compiled python file *.pyc, if the test run is 
#    repeated without changing the test code
ATTACHMENT_EXAMPLE_TEXT= os.path.join(os.path.dirname(__file__), 
                                      'testlinkapi_online_test.py')

class TestLinkAPIOnlineTestCase(unittest.TestCase):
    """ TestCases for TestlinkAPIClient - interacts with a TestLink Server.
    works with the example project NEW_PROJECT_API (see TestLinkExample.py)
    """

    def setUp(self):
        self.client = TestLinkHelper().connect(TestlinkAPIClient)


#    def tearDown(self):
#        pass

    def test_checkDevKey(self):
        response = self.client.checkDevKey()
        self.assertEqual(True, response)
        
    def test_about(self):
        response = self.client.about()
        self.assertIn('Testlink API', response)

    def test_ping(self):
        response = self.client.ping()
        self.assertEqual('Hello!', response)

    def test_echo(self):
        response = self.client.echo('Yellow Submarine')
        self.assertEqual('You said: Yellow Submarine', response)
        
    def test_doesUserExist_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '10000.*Big Bird'):
            self.client.doesUserExist('Big Bird')
        
    def test_getBuildsForTestPlan_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*4711'):
            self.client.getBuildsForTestPlan(4711)
        
    def test_getFirstLevelTestSuitesForTestProject_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*4711'):
            self.client.getFirstLevelTestSuitesForTestProject(4711)

    def test_getFullPath_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, 'getFullPath.*234'):
            self.client.getFullPath('4711')

    def test_getLastExecutionResult_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*4711'):
            self.client.getLastExecutionResult(4711, 4712)
        
    def test_getLatestBuildForTestPlan_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*4711'):
            self.client.getLatestBuildForTestPlan(4711)
        
    def test_getProjects(self):
        response = self.client.getProjects()
        self.assertIsNotNone(response)
        
    def test_getProjectTestPlans_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*4711'):
            self.client.getProjectTestPlans(4711)

    def test_getProjectPlatforms_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*4711'):
            self.client.getProjectPlatforms(4711)
        
    def test_getTestCase_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '5000.*4711'):
            self.client.getTestCase(4711)
        
    def test_getTestCase_unknownExternalID(self):
        with self.assertRaisesRegex(TLResponseError, '5040.*N-2'):
            self.client.getTestCase(testcaseexternalid='N-2')
        
    def test_getTestCaseAttachments_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '5000.*4711'):
            self.client.getTestCaseAttachments(4711)
        
    def test_getTestCaseCustomFieldDesignValue_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*4711'):
            self.client.getTestCaseCustomFieldDesignValue(
                   'TC-4712', 1, 4711, 'a_field', 'a_detail')
        
    def test_getTestCaseIDByName_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '5030.*Cannot find'):
            self.client.getTestCaseIDByName('Big Bird')

    def test_getTestCasesForTestPlan_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*4711'):
            self.client.getTestCasesForTestPlan(4711)

    def test_getTestCasesForTestSuite_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '8000.*4711'):
            self.client.getTestCasesForTestSuite(4711, 2, 'a_detail')

    def test_getTestPlanByName_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7011.*4711'):
            self.client.getTestPlanByName('project 4711', 'plan 4712')

    def test_getTestPlanPlatforms_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*4711'):
            self.client.getTestPlanPlatforms(4711)

    def test_getTestProjectByName_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7011.*4711'):
            self.client.getTestProjectByName('project 4711')

    def test_getTestSuiteByID_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '8000.*4711'):
            self.client.getTestSuiteByID(4711)

    def test_getTestSuitesForTestPlan_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*4711'):
            self.client.getTestSuitesForTestPlan(4711)

    def test_getTestSuitesForTestSuite_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '8000.*4711'):
            self.client.getTestSuitesForTestSuite(4711)

    def test_getTotalsForTestPlan_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*4711'):
            self.client.getTotalsForTestPlan(4711)

    def test_createTestProject_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7001.*Empty name'):
            self.client.createTestProject('', 'P4711')

    def test_createBuild_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*4711'):
            self.client.createBuild(4711, 'Build 4712', 'note 4713')

    def test_createTestPlan_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7011.*4712'):
            self.client.createTestPlan('plan 4711', 'project 4712')

    def test_createTestSuite_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*4711'):
            self.client.createTestSuite( 4711, 'suite 4712', 'detail 4713')

    def test_createTestCase_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*4713'):
            self.client.createTestCase('case 4711', 4712, 4713, 
                                               'Big Bird', 'summary 4714')

    def test_reportTCResult_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '5000.*4711'):
            self.client.reportTCResult(4711, 4712, 'build 4713', 'p', 
                                              'note 4714')

    def test_uploadExecutionAttachment_unknownID(self):
        attachemantFile = open(os.path.realpath(__file__), 'r')
        with self.assertRaisesRegex(TLResponseError, '6004.*4712'):
            self.client.uploadExecutionAttachment(attachemantFile, 4712, 
                        'title 4713', 'descr. 4714')

    def test_getProjectIDByName_unknownID(self):
        response = self.client.getProjectIDByName('project 4711')
        self.assertEqual(-1, response)
        
    def test_createPlatform_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7011.*4711'):
            self.client.createPlatform('Project 4711', 'Platform 4712', 
                                       notes='note 4713')
        
    def test_addTestCaseToTestPlan_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*4711'):
            self.client.addTestCaseToTestPlan(4711, 4712, 'N-4713', 1)
            
    def test_updateTestCase_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '5040.*N-4711'):
            self.client.updateTestCase('N-4711', version=1)

    def test_createTestCaseSteps_unknownID(self):
        steps = [{'actions' : "Step action 6 -b added by updateTestCase" , 
                  'expected_results' : "Step result 6 - b added", 
                  'step_number' : 6, 'execution_type' : 1}]
        with self.assertRaisesRegex(TLResponseError, '5040.*N-4711'):
            self.client.createTestCaseSteps('update', steps, 
                                        testcaseexternalid='N-4711', version=1)
            
    def test_deleteTestCaseSteps_unknownID(self):
        steps = [2,8]
        with self.assertRaisesRegex(TLResponseError, '5040.*N-4711'):
            self.client.deleteTestCaseSteps('N-4711', steps, version=1)

    def test_uploadRequirementSpecificationAttachment_unknownID(self):
        attachemantFile = open(ATTACHMENT_EXAMPLE_TEXT, 'r')
        with self.assertRaisesRegex(TLResponseError, '6004.*4712'):
            self.client.uploadRequirementSpecificationAttachment(attachemantFile, 4712, 
                        title='title 4713', description='descr. 4714')
 
    def test_uploadRequirementAttachment_unknownID(self):
        attachemantFile = open(ATTACHMENT_EXAMPLE_TEXT, 'r')
        with self.assertRaisesRegex(TLResponseError, '6004.*4712'):
            self.client.uploadRequirementAttachment(attachemantFile, 4712, 
                        title='title 4713', description='descr. 4714')
 
    def test_uploadTestProjectAttachment_unknownID(self):
        attachemantFile = open(ATTACHMENT_EXAMPLE_TEXT, 'r')
        with self.assertRaisesRegex(TLResponseError, '7000.*4712'):
            self.client.uploadTestProjectAttachment(attachemantFile, 4712, 
                        title='title 4713', description='descr. 4714')
 
    def test_uploadTestSuiteAttachment_unknownID(self):
        attachemantFile = open(ATTACHMENT_EXAMPLE_TEXT, 'r')
        with self.assertRaisesRegex(TLResponseError, '8000.*4712'):
            self.client.uploadTestSuiteAttachment(attachemantFile, 4712, 
                        title='title 4713', description='descr. 4714')
 
    def test_uploadTestCaseAttachment_unknownID(self):
        attachemantFile = open(ATTACHMENT_EXAMPLE_TEXT, 'r')
        with self.assertRaisesRegex(TLResponseError, '5000.*testcaseid'):
            self.client.uploadTestCaseAttachment(attachemantFile, 4712, 
                        title='title 4713', description='descr. 4714')
 
    def test_uploadAttachment_unknownID(self):
        attachemantFile = open(ATTACHMENT_EXAMPLE_TEXT, 'r')
        with self.assertRaisesRegex(TLResponseError, '6004.*4712'):
            self.client.uploadAttachment(attachemantFile, 4712, 'nodes_hierarchy',
                        title='title 4713', description='descr. 4714')

    def test_testLinkVersion(self):
        response = self.client.testLinkVersion()
        self.assertRegex(response, '\d*\.\d*\.\d*')

    def test_getUserByLogin_unknownKey(self):
        with self.assertRaisesRegex(TLResponseError, '10000.*User Login'):
            self.client.getUserByLogin(user='unknownUser')
            
#     def test_setTestMode(self):
#         response = self.client.setTestMode(True)
#         self.assertTrue(response)
#         response = self.client.setTestMode(False)
#         self.assertTrue(response)
            
    def test_deleteExecution_unknownKey(self):
        try:
            response = self.client.deleteExecution(4711)
            # case: TL configuration allows deletion of executions
            # response returns Success, even if executionID is unkown
            self.assertEqual([{'status': True, 'message': 'Success!', 'id': 4711, 
                               'operation': 'deleteExecution'}], response)
        except TLResponseError as tl_err:
            # case: TL configuration does not allow deletion of executions
            # Expects: 232: Configuration does not allow delete executions
            self.assertEqual(232, tl_err.code)
            
    def test_setTestCaseExecutionType_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*4712'):
            self.client.setTestCaseExecutionType('N-4711', 1, 4712, 1)

    def test_assignRequirements_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*4712'):
            self.client.assignRequirements('N-4711', 4712, 
                        [{'req_spec' : 4713, 'requirements' : [4714, 4717]}, 
                         {'req_spec' : 4723, 'requirements' : [4725]}])
            
    def test_getExecCountersByBuild_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*4711'):
            self.client.getExecCountersByBuild(4711)

    def test_assignTestCaseExecutionTask_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*4711'):
            self.client.assignTestCaseExecutionTask('username', 4711, 'TC-4712', 
                                            buildname='build 4713', 
                                            platformname='platform 4714')                         
            
    def test_getTestCaseBugs_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*4711'):
            self.client.getTestCaseBugs(4711, testcaseexternalid='TC-4712', 
                                        buildname='build 4713',
                                        platformname='platform 4714')                         
                                  
    def test_getTestCaseAssignedTester_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*4711'):
            self.client.getTestCaseAssignedTester(4711, 'TC-4712', 
                                            buildname='build 4713', 
                                            platformname='platform 4714') 
          
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()