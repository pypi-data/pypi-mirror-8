*** Settings *****************************************************************

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Resource  keywords.robot

Test Setup  Open SauceLabs test browser
Test Teardown  Run keywords  Report test status  Close all browsers


*** Test Cases ***************************************************************

Scenario: Disable Generate Tabs in the Navigation Control Panel
  Given a logged-in site administrator
    and a document 'My Document'
    and the navigation control panel
   When I disable generate tabs
   Then the document 'My Document' does not show up in the navigation

Scenario: Enable Folderish Tabs in the Navigation Control Panel
  Given a logged-in site administrator
    and a document 'My Document'
    and the navigation control panel
   When I disable non-folderish tabs
   Then the document 'My Document' does not show up in the navigation

Scenario: Add Document to the Displayed Types in the Navigation Control Panel
  Given a logged-in site administrator
    and a document 'My Document'
    and the navigation control panel
   When I remove 'Document' from the displayed types list
   Then the document 'My Document' does not show up in the navigation


*** Keywords *****************************************************************

# --- GIVEN ------------------------------------------------------------------

the navigation control panel
  Go to  ${PLONE_URL}/@@navigation-controlpanel


# --- WHEN -------------------------------------------------------------------

I disable generate tabs
  Unselect Checkbox  form.widgets.generate_tabs:list
  Click Button  Save
  Wait until page contains  Changes saved

I disable non-folderish tabs
  Unselect Checkbox  xpath=//input[@value='Document']
  Click Button  Save
  Wait until page contains  Changes saved

I remove '${portal_type}' from the displayed types list
  Unselect Checkbox  xpath=//input[@value='Document']
  Click Button  Save
  Wait until page contains  Changes saved


# --- THEN -------------------------------------------------------------------

the document '${title}' does not show up in the navigation
  Go to  ${PLONE_URL}
  Wait until page contains  Powered by Plone
  XPath Should Match X Times  //ul[@id='portal-globalnav']/li/a[contains(text(), '${title}')]  0  message=The global navigation should not have contained the item '${title}'
