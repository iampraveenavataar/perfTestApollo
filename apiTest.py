import boto3
import yaml
from warrant.aws_srp import AWSSRP
import requests
import json
from locust import User, HttpUser, task, between


def prepare_payload(jsonfile):
    with open(f"json/{jsonfile}") as f:
        return json.loads(f.read())


class ApolloLander(HttpUser):
    wait_time = between(0.5, 3)
    def on_start(self):
        # The on_start method is called
        # when a simulated user starts
        # executing that TaskSet class
        yamlFile = "config/config.yaml"
        with open(yamlFile) as f:
            self.config = yaml.load(f, Loader=yaml.SafeLoader)
        client = boto3.client(self.config["idp-host"], region_name=self.config["region_name"])
        self.__aws = AWSSRP(username=self.config["username"], password=self.config["password"],
                            pool_id=self.config["pool_id"], client_id=self.config["client_id"],
                            client=client)
        self.__tokens = self.__aws.authenticate_user()
        with open("json/headers.json") as f:
            self.__headers = json.loads(f.read())
        self.__headers['authorization'] = self.__headers['authorization'].format(
            self.__tokens['AuthenticationResult']['AccessToken'])

    def __init__(self, parent):
        super(ApolloLander, self).__init__(parent)
        self.__aws = None
        self.__tokens = None
        self.__headers = None
        self.config = {}

    @task(3)
    def login(self):
        self.client.get(f"https://{self.config['host']}{self.config['endPoints']['login']}", headers=self.__headers)

    @task(2)
    def authorize(self):
        payload = prepare_payload("user-audit.json")
        self.client.post(f"https://{self.config['host']}{self.config['endPoints']['authorize']}",
                         headers=self.__headers, json=payload)

    @task
    def list_tenants(self):
        payload = prepare_payload("tenant-list-search.json")
        self.client.post(f"https://{self.config['host']}{self.config['endPoints']['listTenants']}",
                             headers=self.__headers, json=payload)

    @task
    def list_experiences_t(self):
        payload = json.loads("""{"isPublic":true}""")
        self.client.post(
            f"https://{self.config['host']}{self.config['endPoints']['list-categories'].format(self.config['tenant_id'])}",
            headers=self.__headers, json=payload)

    @task
    def list_experiences_f(self):
        payload = json.loads("""{"isPublic":false}""")
        self.client.post(
            f"https://{self.config['host']}{self.config['endPoints']['list-categories'].format(self.config['tenant_id'])}",
            headers=self.__headers, json=payload)

    @task
    def search_experiences(self):
        payload = json.loads("""{"isPublic":true,"categories":[],"pagination":{"limit":60,"page":1}}""")
        self.client.post(
            f"https://{self.config['host']}{self.config['endPoints']['search'].format(self.config['tenant_id'])}",
            headers=self.__headers, json=payload)

    @task
    def switch_user(self):
        payload = prepare_payload("signed-urls.json")
        self.client.post(f"https://{self.config['host']}{self.config['endPoints']['switch-tenants']}",
                             headers=self.__headers, json=payload)

    @task
    def open_experience(self):
        payload = prepare_payload("update-experience.json")
        self.client.patch(
            f"https://{self.config['host']}{self.config['endPoints']['Open-update-experience'].format(self.config['tenant_id'], self.config['experience_id'])}",
            headers=self.__headers, json=payload)

    @task
    def add_obj(self):
        payload = prepare_payload("add-object-mesh.json")[0]
        self.client.post(
            f"https://{self.config['host']}{self.config['endPoints']['add-object-mesh'].format(self.config['tenant_id'])}",
            headers=self.__headers, json=payload)

    @task
    def add_3d_mesh(self):
        payload = prepare_payload("add-object-mesh.json")[1]
        self.client.post(
            f"https://{self.config['host']}{self.config['endPoints']['add-object-mesh'].format(self.config['tenant_id'])}",
            headers=self.__headers, json=payload)

    @task
    def fetch_nav(self):
        self.client.get(
            f"https://{self.config['host']}{self.config['endPoints']['fetch-nav'].format(self.config['tenant_id'])}",
            headers=self.__headers)

# ap = ApolloLander()
# print(ap.login().status_code)
# print(ap.authorize().status_code)
# print(ap.list_experiences_t().text)
# print(ap.list_experiences_f().text)
# print(ap.search_experiences().text)
# print(ap.open_experience().status_code)
# print(ap.add_obj().status_code)
# print(ap.add_3d_mesh().status_code)
# print(ap.fetch_nav().status_code)
