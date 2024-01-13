@directory
Feature: Ability to interact with a Directory service

Background:
     Given The service proxy is defined in user configuration PROXY
       And The service proxy belongs to a Directory service
      When I ask for joseluis's root directory
      Then The retrieved directory is valid

  Scenario: Get the root directory for a new user
      Then The retrieved directory has 0 files
       And The retrieved directory has 0 child directories
      When I navigate to parent directory
      Then The operation raises RootHasNoParent

  Scenario: Prepare the directory structure
      When I add a link to abcdefgh named file1 to the retrieved directory
      Then The operation returns no error
      When I add a link to ijklmnop named file2 to the retrieved directory
      Then The operation returns no error
      When I add a child directory named dir1 to the retrieved directory
      Then The operation returns no error
      When I add a child directory named dir2 to the retrieved directory

  Scenario: When retrieve the root directory for second time, it keeps the state
      Then The retrieved directory has 2 file
       And The retrieved directory has 2 child directories

  Scenario: A directory is able to return its child directories
      Then The retrieved directory has the following child directories
      | directory |
      | dir1      |
      | dir2      |

  Scenario: A directory is able to return its list of archives
      Then The retrieved directory has the following archives
      | archives |
      | file1    |
      | file2    |

  Scenario: The returned blob_id is the expected
      When I want to get the blob id of a file named file2
      Then The received blob_id is ijklmnop
      When I want to get the blob id of a file named file1
      Then The received blob_id is abcdefgh

  Scenario: After unlinking a file, the getBlobId fails
      When I remove a link named file2 from the retrieved directory
       And I want to get the blob id of a file named file2
      Then The operation raises FileNotFound

  Scenario: Retrieve a non-existant directory
      When I want to access the child directory named non-existant
      Then The operation raises ChildNotExists

  Scenario: Retrieve a non-existant file
      When I want to get the blob id of a file named non-existant
      Then The operation raises FileNotFound

  Scenario: Create an already existing directory
      When I add a child directory named dir1 to the retrieved directory
      Then The operation raises ChildAlreadyExists

  Scenario: Repeat a link will fails
      When I add a link to ijklmnop named file1 to the retrieved directory
      Then The operation raises FileAlreadyExists

  Scenario: Remove a child directory
      When I remove a child directory named dir2 from the retrieved directory
      Then The operation returns no error

  Scenario: The removed child is not shown in getChilds output
      Then The retrieved directory has the following child directories
      | directory |
      | dir1      |

  Scenario: Remove all the files and directories to return to the initial state
      When I remove a child directory named dir1 from the retrieved directory
      When I remove a link named file1 from the retrieved directory

  Scenario: Remove a non-existing file
      When I remove a link named non-existing from the retrieved directory
      Then The operation raises FileNotFound

  Scenario: After removing everything, the root directory has no files
      Then The retrieved directory has 0 files

  Scenario: Create a directory structure and check it in the following scenarios
      When I add a child directory named subdir to the retrieved directory
      Then The operation returns no error
      When I want to access the child directory named subdir
      Then The operation returns no error
      When I add a child directory named grandson to the retrieved directory
      Then The operation returns no error
      When I want to access the child directory named grandson
      Then The operation returns no error
      When I add a link to abcdefgh named file1 to the retrieved directory
      Then The operation returns no error
       And The retrieved directory has the following archives
      | archives |
      | file1    |
      When I navigate to parent directory
