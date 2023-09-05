import boto3
import yaml
from warrant.aws_srp import AWSSRP
import json
from locust import FastHttpUser, task, tag

FastHttpUser.concurrency=10000

# stats.CSV_STATS_INTERVAL_SEC = 5  # default is 1 second
# stats.CSV_STATS_FLUSH_INTERVAL_SEC = 60


def prepare_payload(jsonfile):
    with open(f"json/{jsonfile}") as f:
        return json.loads(f.read())


class ApolloLander(FastHttpUser):
    # wait_time = between(0.5, 3)
    def on_start(self):
        yamlFile = "config/config.yaml"
        with open(yamlFile) as f:
            self.config = yaml.load(f, Loader=yaml.SafeLoader)
        client = boto3.client(self.config["idp-host"], region_name=self.config["region_name"])
        self.__aws = AWSSRP(username=self.config["username"], password=self.config["password"],
                            pool_id=self.config["pool_id"], client_id=self.config["client_id"],
                            client=client)
        self.__tokens = self.__aws.authenticate_user()
        self.__headers=prepare_payload("headers.json")
        self.__headers['authorization'] = self.__headers['authorization'].format(
            self.__tokens['AuthenticationResult']['AccessToken'])

    def __init__(self, parent):
        super(ApolloLander, self).__init__(parent)
        self.__aws = None
        self.__tokens = None
        self.__headers = None
        self.config = {}

    @tag('apheleia')
    @task(3)
    def login(self):
        self.client.get(f"https://{self.config['host']}{self.config['endPoints']['login']}", headers=self.__headers)

    # @tag('apheleia')
    # @task(2)
    # def authorize(self):
    #     payload = prepare_payload("user-audit.json")
    #     self.client.post(f"https://{self.config['host']}{self.config['endPoints']['authorize']}",
    #                      headers=self.__headers, json=payload)

    @tag('apheleia')
    @task
    def list_tenants(self):
        payload = prepare_payload("tenant-list-search.json")
        self.client.post(f"https://{self.config['host']}{self.config['endPoints']['listTenants']}",
                         headers=self.__headers, json=payload)

    @tag('apollo')
    @task
    def list_experiences_exposed(self):
        payload = json.loads("""{"isPublic":true}""")
        self.client.post(
            f"https://{self.config['host']}{self.config['endPoints']['list-categories'].format(self.config['tenant_id'])}",
            headers=self.__headers, json=payload)

    @tag('apollo')
    @task
    def list_experiences_implicit(self):
        payload = json.loads("""{"isPublic":false}""")
        self.client.post(
            f"https://{self.config['host']}{self.config['endPoints']['list-categories'].format(self.config['tenant_id'])}",
            headers=self.__headers, json=payload)

    @tag('apollo')
    @task
    def switch_user(self):
        payload = prepare_payload("signed-urls.json")
        self.client.post(f"https://{self.config['host']}{self.config['endPoints']['switch-tenants']}",
                         headers=self.__headers, json=payload)

    @tag('apollo')
    @task
    def fetch_nav(self):
        self.client.get(
            f"https://{self.config['host']}{self.config['endPoints']['fetch-nav'].format(self.config['tenant_id'])}",
            headers=self.__headers)

    @tag('apollo')
    @task
    def image_2_3d(self):
        payload = json.loads("""{"filters":{"stages":["IMG_TO_3D_IN_PROGRESS"]}}""")
        self.client.post(
            f"https://{self.config['host']}{self.config['endPoints']['search-img-2-3d'].format(self.config['tenant_id'])}",
            headers=self.__headers, json=payload)

    @tag('apollo')
    @task
    def new_records(self):
        self.client.post(
            f"https://{self.config['host']}{self.config['endPoints']['new-records'].format(self.config['tenant_id'])}",
            headers=self.__headers)

    @tag('experience')
    @task
    def search_experiences_pub(self):
        payload = prepare_payload("experience-search.json")[0]
        self.client.post(
            f"https://{self.config['host']}{self.config['endPoints']['search'].format(self.config['tenant_id'])}",
            headers=self.__headers, json=payload)

    @tag('experience')
    @task
    def search_experiences_pvt(self):
        payload = prepare_payload("experience-search.json")[1]
        self.client.post(
            f"https://{self.config['host']}{self.config['endPoints']['search'].format(self.config['tenant_id'])}",
            headers=self.__headers, json=payload)

    @tag('experience')
    @task
    def open_experience(self):
        payload = prepare_payload("update-experience.json")
        self.client.patch(
            f"https://{self.config['host']}{self.config['endPoints']['Open-update-experience'].format(self.config['tenant_id'], self.config['experience_id'])}",
            headers=self.__headers, json=payload)

    @tag('editor')
    @task
    def add_obj(self):
        payload = prepare_payload("add-object-mesh.json")[0]
        self.client.post(
            f"https://{self.config['host']}{self.config['endPoints']['add-object-mesh'].format(self.config['tenant_id'])}",
            headers=self.__headers, json=payload)

    @tag('editor')
    @task
    def add_3d_mesh(self):
        payload = prepare_payload("add-object-mesh.json")[1]
        self.client.post(
            f"https://{self.config['host']}{self.config['endPoints']['add-object-mesh'].format(self.config['tenant_id'])}",
            headers=self.__headers, json=payload)

    @tag('polygons')
    @task
    def add_room_pub(self):
        payload = prepare_payload("add-rooms.json")[0]
        self.client.post(
            f"https://{self.config['host']}{self.config['endPoints']['add-rooms'].format(self.config['tenant_id'])}",
            headers=self.__headers, json=payload)

    @tag('polygons')
    @task
    def add_room_pvt(self):
        payload = prepare_payload("add-rooms.json")[1]
        self.client.post(
            f"https://{self.config['host']}{self.config['endPoints']['add-rooms'].format(self.config['tenant_id'])}",
            headers=self.__headers, json=payload)

