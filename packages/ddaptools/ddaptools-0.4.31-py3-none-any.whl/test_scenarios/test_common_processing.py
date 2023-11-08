from ddaptools.aws_classes.class_enhancement import *
from ddaptools.dda_constants import *


def run_procesing(staging_guid = "42c6cd4b-a6ea-4087-ab6a-b8b5bed8b256"):
    """
    1. Email event.
    2. Publishes in database should result in updated start and updated endtime.
    """
    

    credentials = {
        'USERNAME': "postgres",
        'PASSWORD': "dDueller123araM=!",
        "HOST": "stage-dd-portal-database.cby8aaf6nvlw.us-east-1.rds.amazonaws.com",
        "DB": "v1_2"
    }

    settings = {
        "GET_TABLENAME": "staging_events",
        "TABLENAME_EVENTS": "event",
        "COLUMN_NAMES_EVENTS": Event.get_attribute_keys(),
        "TABLENAME_TIMESLOTS": "timeslot",
        "COLUMN_NAMES_TIMESLOTS": Timeslot.get_attribute_keys()
    }

    
    organizationDBProvider = PostgresqlOrganizationQuerier(credentials=credentials)

    publishingDBProvider = PostgreSQLProviderTimeSlotPlusEventsPublishing(credentials=credentials, settings=settings)

    # Salesforce Sample:  588e876e-31e6-91d4-863f-e0986fd90dad
    processor = PostgresS3ConnectorBasedCommonProcessor(
        
        job_parameters={"guid": staging_guid},
        organization_provider=organizationDBProvider,
        publishingDBProvider=publishingDBProvider
    ) 
    
    processor.runJobs() # Should also post at the Mock Database




def test_multiple():
    staging_list = [
        # '8d908be7-95d9-4edf-a355-6f817f6587ec'
        # 'd1cbca0a-e74f-46c3-849d-972d4c486b83'
        # '387f2a2b-0d2f-443d-be42-500ff304ef38'

        # '014bb5b2-60ed-494e-a5d0-507efb63592e',
        # 'dca4d47f-12b5-4946-acd3-c402d53b567a',
        # 'e5e4b6f2-032e-4e33-a588-f429fe7f7a2f',
        'dc16c68d-a5af-4940-b57e-1011eab58451',
        'f3a8b56a-a0a0-47ba-ae2a-d237bf11f364'
    ]

    for staging_guid in staging_list:
        print("Processing: ", staging_guid)
        run_procesing(staging_guid=staging_guid)






