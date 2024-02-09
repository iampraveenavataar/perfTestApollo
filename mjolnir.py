import requests
import json
import random
from concurrent.futures import ThreadPoolExecutor

from locust import FastHttpUser, task, tag


class mjolnir1(FastHttpUser):
    url = "http://apheleia-qa-alb-1540983728.us-east-1.elb.amazonaws.com/user"
    @task
    def fire(self):
        # Dictionary of API endpoints and corresponding authorization tokens
        # url = self.client.base_url

        with open("json/tokens.json") as f:
            api_tokens = json.loads(f.read())
        headers = {'Authorization': f'Bearer {api_tokens[random.choice(list(api_tokens.keys()))]}'}
        self.client.get(self.url, headers=headers)


class mjolnir2(FastHttpUser):
    url = "http://apheleia-rust-qa-alb-1228403005.us-east-1.elb.amazonaws.com/user"
    @task
    def fire(self):
        # Dictionary of API endpoints and corresponding authorization tokens
        # url = self.client.base_url

        with open("json/tokens.json") as f:
            api_tokens = json.loads(f.read())
        headers = {'Authorization': f'Bearer {api_tokens[random.choice(list(api_tokens.keys()))]}'}
        self.client.get(self.url, headers=headers)
