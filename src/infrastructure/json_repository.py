
import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from src.domain.models import BinaryFile

class JsonRepository(object):

    def __init__(self, json_path="database.json"):
        self.json_path = json_path
        #self.__ensure_database()

    def __ensure_database(self) -> None:
        """Ensure the database file and its directory exist."""
        directory = os.path.dirname(self.json_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        if not os.path.exists(self.json_path):
            with open(self.json_path, "w", encoding="utf-8") as db_file:
                json.dump([], db_file, indent=4)

    def __load_data(self) -> List[Dict[str, Any]]:
        with open(self.json_path, "r", encoding="utf-8") as db_file:
            content = db_file.read().strip()
            return json.loads(content) if content else []

    def __save_data(self, data: List[Dict[str, Any]]) -> None:
        with open(self.json_path, "w", encoding="utf-8") as db_file:
            json.dump(data, db_file, indent=4, ensure_ascii=False)

    def add_record(self, record: Any) -> None:
        """
        Add a new record to the JSON database.
        Accepts either a BinaryFile instance or a dictionary.
        """
        data = self.__load_data()

        if isinstance(record, BinaryFile):
            record = record.to_dict()

        record["uploaded_at"] = datetime.now().isoformat()
        data.append(record)
        self.__save_data(data)

    def get_record(self, file_id: str) -> Optional[BinaryFile]:
        """Retrieve a record and return it as a BinaryFile."""
        data = self.__load_data()
        for entry in data:
            if entry.get("id") == file_id:
                return BinaryFile.from_dict(entry)
        return None

    def list_records(self) -> List[BinaryFile]:
        """Return all records as a list of BinaryFile instances."""
        data = self.__load_data()
        return [BinaryFile.from_dict(entry) for entry in data]

    def update_record(self, file_id: str, updates: Dict[str, Any]) -> bool:
        data = self.__load_data()
        for entry in data:
            if entry.get("id") == file_id:
                entry.update(updates)
                self.__save_data(data)
                return True
        return False

    def delete_record(self, file_id: str) -> bool:
        data = self.__load_data()
        new_data = [entry for entry in data if entry.get("id") != file_id]
        if len(new_data) != len(data):
            self.__save_data(new_data)
            return True
        return False