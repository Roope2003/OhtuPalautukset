*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  newuser
    Set Password  ValidPass123
    Set Password Confirmation  ValidPass123
    Click Button  Register
    Registration Should Succeed With Message  Welcome to Ohtu Application!


Register With Too Short Username And Valid Password
    Set Username  nu
    Set Password  ValidPass123
    Set Password Confirmation  ValidPass123
    Click Button  Register
    Registration Should Fail With Message  Käyttäjätunnuksen on oltava vähintään 3 merkkiä pitkä    


Register With Valid Username And Too Short Password
    Set Username  validuser
    Set Password  short
    Set Password Confirmation  short
    Click Button  Register
    Registration Should Fail With Message  Salasanan on oltava vähintään 8 merkkiä pitkä    


Register With Valid Username And Invalid Password
# salasana ei sisällä halutunlaisia merkkejä
    Set Username  validuser
    Set Password  password
    Set Password Confirmation  password
    Click Button  Register
    Registration Should Fail With Message  Salasana ei voi koostua pelkästään kirjaimista


Register With Nonmatching Password And Password Confirmation
    Set Username  validuser
    Set Password  ValidPass123
    Set Password Confirmation  DifferentPass123
    Click Button  Register
    Registration Should Fail With Message  Salasanat eivät täsmää


Register With Username That Is Already In Use
    Create User  existinguser  ExistingPass123
    Set Username  existinguser
    Set Password  NewPass123
    Set Password Confirmation  NewPass123
    Click Button  Register
    Registration Should Fail With Message  Käyttäjätunnus on jo käytössä




*** Keywords ***
Reset Application Create User And Go To Register Page
    Go To Starting Page
    Reset Application
    Go To Register Page

Go To Register Page
    Go To  ${REGISTER_URL}
    

Set Username
    [Arguments]  ${username}
    Input Text  id=username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  id=password  ${password}

Set Password Confirmation
    [Arguments]  ${password_confirmation}
    Input Password  id=password_confirmation  ${password_confirmation}

Registration Should Succeed With Message
    [Arguments]  ${message}
    Title Should Be  Welcome to Ohtu Application!
    Page Should Contain  ${message}    

Registration Should Fail With Message
    [Arguments]  ${message}
    Title Should Be  Register
    Page Should Contain  ${message}