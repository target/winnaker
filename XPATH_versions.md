## XPATH Verions


As Spinnaker is updated we will document older versions of XPATHs as the deck component is updated, XPATHs are current for version 1.x of Halyard installs of Spinnaker


The older XPATHs are documented for older versions of deck


| ENV VAR NAME | XPATH|
| :-----------: | :--------:
| WINNAKER_XPATH_LOGIN_USERNAME | //input[@id='username'][@name='pf.username'] |
| WINNAKER_XPATH_LOGIN_PASSWORD | //input[@id='password'][@name='pf.pass'] |
| WINNAKER_XPATH_LOGIN_SUBMIT | //input[@type='submit'] |
| WINNAKER_XPATH_APPLICATIONS_TAB | //a[@href='#/applications' and contains(.,'Applications')] |
| WINNAKER_XPATH_SEARCH_APPLICATIONS | //input[@placeholder='Search applications'] |
| WINNAKER_XPATH_START_MANUAL_EXECUTION | //div[contains(@class, 'execution-group-actions')]/h4[2]/a/span |
| WINNAKER_XPATH_FORCE_REBAKE | //input[@type='checkbox' and @ng-model='vm.command.trigger.rebake'] |
| WINNAKER_XPATH_PIPELINE_EXECUTION_SUMMARY | //execution[1]//div[@class='execution-summary'] |
| WINNAKER_XPATH_PIPLELINE_TRIGGER_DETAILS | //execution[1]//ul[@class='trigger-details'] |
| WINNAKER_XPATH_PIPLELINE_DETAILS_LINK | //execution[1]//execution-status//div/a[contains(., 'Details')] |
