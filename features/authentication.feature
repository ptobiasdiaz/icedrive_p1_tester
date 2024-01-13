@auth
Feature: Ability to interact with an Authentication service

Background:
     Given The service proxy is defined in user configuration PROXY
       And The service proxy belongs to an Authentication service

  Scenario: Succesfully user creation
      When I create an user named joseluis with password 1234
      Then The retrieved user is valid
       And The retrieved user is alive

   Scenario: The User object can be verified
      When I login as user joseluis using password 1234
      Then The retrieved user can be verified

   Scenario: A self stored User object cannot be verified
      When I create a self stored User
      Then The retrieved user cannot be verified

   Scenario: An invented User object cannot be verified
      When I create a non-accesible User
      Then The retrieved user cannot be verified

  Scenario: Repeat uset creation fails
      When I create an user named joseluis with password whocares
      Then The user creation returned UserAlreadyExists exception

   Scenario: Succesfully login
      When I login as user joseluis using password 1234
      Then The retrieved user is valid
       And The retrieved user is alive
       And The retrieved user's username is joseluis

   Scenario: User expires after 2 minutes
      When I login as user joseluis using password 1234
       And I wait for 121 seconds
      Then The retrieved user is not alive
      When I refresh the retrieved user
      Then The refresh fails with Unauthorized exception

   Scenario: User is able to extend the validity using refresh
      When I login as user joseluis using password 1234
       And I wait for 60 seconds
       And I refresh the retrieved user
       And I wait for 61 seconds
      Then The retrieved user is alive
      When I wait for 61 seconds
      Then The retrieved user is not alive

   Scenario: Unsuccesful login with incorrect password
      When I login as user joseluis using password wrongpassword
      Then The login fails with Unauthorized exception

   Scenario: Unsuccesful login with incorrect username
      When I login as user wronguser using password wrongpassword
      Then The login fails with Unauthorized exception

   Scenario: User deletion with wrong credentials fails
      When I remove an user named joseluis with password wrongpassword
      Then The remove fails with Unauthorized exception

   Scenario: User deletion
      When I remove an user named joseluis with password 1234
       And I login as user joseluis using password 1234
      Then The login fails with Unauthorized exception
