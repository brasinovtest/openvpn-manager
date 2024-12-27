import math
from abc import abstractmethod
from datetime import datetime

class Parser:

    def __init__(self, output: str) -> None:
        self.output = output

    @abstractmethod
    def parse(self):
        pass

class ParseStatusOutput(Parser):

    @staticmethod
    def convert_size(size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    @staticmethod
    def parse_status_to_list(data: str, status: str) -> list:
        return [item.split(',')[1:] for item in data.splitlines() if status in item]

    def parse_status_to_dict(self, data: str, status: str) -> list[dict]:
        data_list = self.parse_status_to_list(data, status)
        return [{data_list[0][item.index(value)].replace(' ', ''): value for value in item} for item in data_list[1:]]

    @staticmethod
    def calculate_connection_duration(date_one: str, date_two: str) -> str:
        date_one = datetime.strptime(date_one, "%Y-%m-%d %H:%M:%S")
        date_two = datetime.strptime(date_two, "%Y-%m-%d %H:%M:%S")
        return str(date_two - date_one)

    def parse_status_to_json(self, client_list: str, routing_list: str) -> list:
        client_list = self.parse_status_to_dict(client_list, 'CLIENT_LIST')
        routing_list = self.parse_status_to_dict(routing_list, 'ROUTING_TABLE')
        response = []
        for client in client_list:
            for routing in routing_list:
                if client.get('CommonName') == routing.get('CommonName'):
                    item = {**client, **routing}
                    item['BytesReceived'] = self.convert_size(int(item['BytesReceived']))
                    item['BytesSent'] = self.convert_size(int(item['BytesSent']))
                    item['HowLong'] = self.calculate_connection_duration(item['ConnectedSince'], item['LastRef'])
                    response.append(item)
        return response

    def parse(self):
        client_list, route_table = self.output.split('HEADER,')[1:]
        return self.parse_status_to_json(client_list, route_table)


def parser_factory(method: str, output: str) -> Parser:
    match method:
        case "status": return ParseStatusOutput(output)
        case "help": return ParseStatusOutput(output)
        case _: raise AttributeError(f'{method} is not a valid method')


__all__ = ['parser_factory']
