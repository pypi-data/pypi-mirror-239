import sys
import json
import requests
import argparse


class OlcRunner():

    host = "localhost"
    port = 8888
    model = "llama2"

    endpoint_generate = "api/generate"

    def run(self):
        
        parser = argparse.ArgumentParser(description='ollama command line utility.')
        parser.add_argument('prompt', type=str, help='Required prompt to be send to the ollama model.')
        parser.add_argument('--model', type=str, help=f'The name of the ollama model to use. Default is "{self.model}".', default=self.model)
        parser.add_argument('--host', type=str, help=f'The hostname where ollama serve is running. Default is "{self.host}".', default=self.host)
        parser.add_argument('--port', type=int, help=f'The port where ollama serve is running. Default is "{self.port}".', default=self.port)
        # TODO: add llm arguments like temp
        parser.add_argument('--sync', action='store_true', help='This switch executes the query synchronous.')
        
        args = parser.parse_args()
        
        prompt = args.prompt
        if (len(args.prompt) == 0):
            parser.error("Please provide a prompt for the model.")
        
        self.host = args.host
        self.port = args.port
        
        if not self._is_ollama_running():
            parser.error(f'Ollama is not running at expected address "{self._get_endpoint()}"')

        if (args.sync):
            print(self._generate(prompt))
        else:
            self._generate_async(prompt)

    def _generate_async(self, prompt: str) -> str:
        request_body = self._get_generate_request_body(prompt, stream=True)
        try:
            result = requests.post(f"{self._get_endpoint()}/{self.endpoint_generate}", data=json.dumps(request_body), stream=True)
            if result.status_code != 200:
                raise RuntimeError(f"Unexpected status code: {result.status_code} - {result.text}")

            for line in result.iter_lines():
                line_str = line.decode('UTF-8')
                line_json = json.loads(line_str)
                response = line_json['response']
                print(response, end="")

        except Exception as ex:
            raise RuntimeError(ex)

    def _generate(self, prompt: str) -> str:
        request_body = self._get_generate_request_body(prompt, stream=False)

        try:
            result = requests.post(f"{self._get_endpoint()}/{self.endpoint_generate}", data=json.dumps(request_body))
            if result.status_code != 200:
                raise RuntimeError(f"Unexpected status code: {result.status_code} - {result.text}")

            as_array = result.text.replace("}\n{", "},\n{")
            result_json: dict = json.loads(f"[{as_array}]")

            response = ""
            for item in result_json:
                response += item['response']

            return response
        except Exception as ex:
            raise RuntimeError(ex)

    def _get_generate_request_body(self, prompt: str, stream: bool = False) -> str:
        return {
            "model": self.model,
            "prompt": prompt,
            "stream": stream
        }

    def _is_ollama_running(self) -> bool:
        try:
            result = requests.get(f"{self._get_endpoint()}/")
            return result.status_code == 200
        except Exception as ex:
            print(ex)
            return False

    def _get_endpoint(self) -> str:
        return f'http://{self.host}:{self.port}'

def run():
    OlcRunner().run()


if __name__ == '__main__':
    OlcRunner().run()
