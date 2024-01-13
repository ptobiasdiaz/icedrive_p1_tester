# icedrive: a file and directory service using ZeroC Ice

This repository contains the implementation of the `icedrive` proposed laboratory.

## Definition of the service

`icedrive` consists on 3 different services that will interact between them to offer an
online storage solution with support for files and directories. Those 3 services will be:

- An auhentication service that allows the users to register and login in the system
    with the credentials. This service will be in charge of validating the users for the
    rest of the services too.

- A file storage service, that allows the users to upload or remove files into the storage.
- A directory service, that will handle the directories that each user owns in the system,
    allowing the users to add subdirectories at any level, adding files into each directory,
    etc.

## Implementation of the services

The services will be implemented in Python 3.9 or later, using ZeroC Ice 3.7 as RMI middleware.

## Run the BDD tests

1. Install the dependencies with `pip install .[bdd_tests]`
1. Run the tests with `behave -t SERVICE -D "PROXY=service_proxy"` where:
    - `SERVICE` is `auth`, `directory`, `blob` or `blob_restart` for checking persistance requirements.
    - `service_proxy` is the stringfied proxy for the service under test.
