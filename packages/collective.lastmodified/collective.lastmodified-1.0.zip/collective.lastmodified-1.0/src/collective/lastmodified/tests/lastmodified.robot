*** Settings ***
Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot

Library  Remote  ${PLONE_URL}/RobotRemote
Library  plone.app.robotframework.keywords.Debugging

Suite Setup  Start browser
Suite Teardown  Close All Browsers

*** Variables ***

${DOC_TITLE}  A test document
${DOC_ID}  a-test-document

*** Test Cases ***

Test Document Edit
    Go to  ${PLONE_URL}/createObject?type_name=Document
    Page Should Contain Checkbox  id=showLastModified

Test Viewlet Behaviour
    Create Test Document
    Page should not contain element  id=plone-document-lastmodified

    Activate Viewlet
    Element Should Be Visible  id=plone-document-lastmodified

    Deactivate Viewlet
    Page should not contain element  id=plone-document-lastmodified

*** Keywords ***

Start browser
    Open browser  http://localhost:55001/plone/
    Enable autologin as  Manager

Create Test Document
    Add document  ${DOC_TITLE}

Activate Viewlet
    Go to  ${PLONE_URL}/${DOC_ID}/edit
    Click Link  id=fieldsetlegend-settings
    Select Checkbox  id=showLastModified
    Click button  name=form.button.save

Deactivate Viewlet
    Go to  ${PLONE_URL}/${DOC_ID}/edit
    Click Link  id=fieldsetlegend-settings
    Unselect Checkbox  id=showLastModified
    Click button  name=form.button.save
