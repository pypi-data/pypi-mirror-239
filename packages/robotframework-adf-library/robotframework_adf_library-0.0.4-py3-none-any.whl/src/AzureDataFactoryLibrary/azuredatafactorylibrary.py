from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.identity import DefaultAzureCredential
from robot.api import logger
from robot.api.deco import library, keyword
from datetime import timedelta, date
import time


@library
class AzureDataFactoryLibrary():
    ROBOT_LIBRARY_SCOPE = 'SUITE'

    def __init__(self):
        self.credential = None
        self.client = None
        self.resource_group_name = None
        self.datafactory_name = None

    @keyword
    def connect_to_adf(self, subscription_id: str, resource_group_name: str, datafactory_name: str):
        self.resource_group_name = resource_group_name
        self.datafactory_name = datafactory_name
        self.credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
        self.client = DataFactoryManagementClient(credential=self.credential, subscription_id=subscription_id)

    @keyword
    def get_pipelines_of_adf_instance(self, resource_group_name: str, datafactory_name: str):
        pipelines = self.client.pipelines.list_by_factory(resource_group_name=resource_group_name,
                                                          factory_name=datafactory_name)
        return pipelines

    @keyword
    def start_pipeline_and_wait_for_completion(self, pipeline_name: str, parameters: dict, refresh_rate: timedelta,
                                               timeout: timedelta):
        run_id = self.client.pipelines.create_run(self.resource_group_name, self.datafactory_name, pipeline_name,
                                                  parameters=parameters).run_id
        seconds_run = 0
        while seconds_run < timeout.total_seconds():
            status = self.get_status_of_pipeline(run_id)
            if status == "Succeeded" or status == "Failed" or status == "Cancelled":
                logger.info('pipeline: {} met run_id: {} is afgerond met status: {}'.format(pipeline_name, run_id, status))
                return status
            logger.info('pipeline: {} met run_id: {} heeft nu status: {}'.format(pipeline_name, run_id, status))
            time.sleep(refresh_rate.total_seconds())
            seconds_run += refresh_rate.total_seconds()

    def get_status_of_pipeline(self, run_id: str):
        status = self.client.pipeline_runs.get(self.resource_group_name, self.datafactory_name, run_id).status
        return status
