*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${web_url}  http://127.0.0.1:5000

*** Test Cases ***
Guest User Test
    [Documentation]  This test is for guest
    [Tags]  user
    Open Browser    ${web_url}   chrome
    Click Element  xpath=//html/body/div[2]/div/div/div/form/table/tbody/tr[4]/td[2]/a
    sleep  1s
    Click Element  xpath=//html/body/div[2]/div/div/form/table/tbody/tr[5]/td[2]/a
    sleep  1s
    Test 1 Description
    sleep  1s
    Test 1 Remark
    sleep  1s
    Click

User Register Test
    [Documentation]  This test is to register user
    [Tags]  user


Registered User Login Test
    [Documentation]  This test is to login user
    [Tags]  user

User Report Crime Test
    [Documentation]  This test is to report crime
    [Tags]  user

User Modify Test
    [Documentation]  This test is for modification
    [Tags]  user

User Logout
    [Documentation]  This test is to logout
    [Tags]  user

Admin Login Test
    [Documentation]  This test is for admin login
    [Tags]  admin

Admin View Report Test
    [Documentation]  This test is to view report
    [Tags]  admin

Admin Search Report Test
    [Documentation]  This test is to search report
    [Tags]  admin

Admin Logout
    [Documentation]  This test to logout admin
    [Tags]  admin


*** Keywords ***
Test 1 Description
    Input Text  name:description  robbery
Test 1 Remark
    Input Text  name:remark  chain

