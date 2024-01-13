@blob

Feature: Ability to interact with a Blob service

Background:
     Given The service proxy is defined in user configuration PROXY
       And The service proxy belongs to a Blob service

  Scenario: Download an unknown blob id fails
      When I download a blob identified by 123456
      Then The operation raises UnknownBlob

  Scenario: Link an unknown blob id fails
      When I add a link to a blob identified by 123456
      Then The operation raises UnknownBlob

  Scenario: Unlink an unknown blob id fails
      When I remove a link to a blob identified by 123456
      Then The operation raises UnknownBlob

  Scenario: Upload a blob and get the blob_id
      When I upload a blob with the following content
      """
      This is the content of my blob

      """
      Then The generated blob id is 01c3437490e153f1e9be3eb3efdb350ed7dbbede1fb001dc4d336c74a6e1e736
       And The operation returns no error
       And The DataTransfer object was closed

  @blob_restart
  Scenario: Download a blob
      When I download a blob identified by 01c3437490e153f1e9be3eb3efdb350ed7dbbede1fb001dc4d336c74a6e1e736
      Then The operation returns no error
      Then The downloaded content is
      """
      This is the content of my blob

      """
       And The downloaded content SHA256 is 01c3437490e153f1e9be3eb3efdb350ed7dbbede1fb001dc4d336c74a6e1e736

  @blob_restart
  Scenario: Link an known blob id works
      When I add a link to a blob identified by 01c3437490e153f1e9be3eb3efdb350ed7dbbede1fb001dc4d336c74a6e1e736
      Then The operation returns no error

  @blob_restart
  Scenario: Unlink an known blob id works
      When I remove a link to a blob identified by 01c3437490e153f1e9be3eb3efdb350ed7dbbede1fb001dc4d336c74a6e1e736
      Then The operation returns no error

  @blob_restart
  Scenario: After unlinking the last one, file should be removed
      When I remove a link to a blob identified by 01c3437490e153f1e9be3eb3efdb350ed7dbbede1fb001dc4d336c74a6e1e736
      Then The operation raises UnknownBlob

  Scenario: Upload again to prepare restart
      When I upload a blob with the following content
      """
      This is the content of my blob

      """
      Then The generated blob id is 01c3437490e153f1e9be3eb3efdb350ed7dbbede1fb001dc4d336c74a6e1e736
       And The operation returns no error
       And The DataTransfer object was closed
