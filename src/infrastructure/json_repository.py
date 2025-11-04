
import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

class JsonRepository(object):

    def __init__(self, json_path: str = "database.json"):
        self.json_path = json_path
        self.__ensure_database()

    def __ensure_database(self) -> None:
        directory = os.path.dirname(self.json_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(self.json_path):
            with open(self.json_path, "w", encoding="utf-8") as db_file:
                json.dump([], db_file, indent=4)

    def __load_data(self) -> List[Dict[str, Any]]:
        with open(self.json_path, "r", encoding="utf-8") as db_file:
            return json.load(db_file)

    def __save_data(self, data: List[Dict[str, Any]]) -> None:
        with open(self.json_path, "w", encoding="utf-8") as db_file:
            json.dump(data, db_file, indent=4, ensure_ascii=False)

    def add_record(self, record: Dict[str, Any]) -> None:
        data = self.__load_data()
        record["timestamp"] = datetime.now().isoformat()
        data.append(record)
        self.__save_data(data)

    def get_record(self, file_id: str) -> Optional[Dict[str, Any]]:
        data = self.__load_data()
        for entry in data:
            if entry.get("file_id") == file_id:
                return entry
        return None

    def update_record(self, file_id: str, updates: Dict[str, Any]) -> bool:
        data = self.__load_data()
        for entry in data:
            if entry.get("file_id") == file_id:
                entry.update(updates)
                self.__save_data(data)
                return True
        return False

    def list_records(self) -> List[Dict[str, Any]]:
        return self.__load_data()

    def delete_record(self, file_id: str) -> bool:
        data = self.__load_data()
        new_data = [entry for entry in data if entry.get("file_id") != file_id]

        if len(new_data) != len(data):
            self.__save_data(new_data)
            return True
        return False