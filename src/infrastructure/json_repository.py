import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional


class JsonRepository(object):
    def __init__(self, json_path: str = "database.json"):
        self.json_path = json_path
        self.__ensure_database()

    def __ensure_database(self) -> None:
        """Garantiza que exista la ruta y el archivo JSON."""
        directory = os.path.dirname(self.json_path)

        # Solo crea carpetas si el path tiene directorio
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(self.json_path):
            with open(self.json_path, "w", encoding="utf-8") as db_file:
                json.dump([], db_file, indent=4)

    def __load_data(self) -> List[Dict[str, Any]]:
        """Carga el contenido del JSON como lista de diccionarios."""
        if not os.path.exists(self.json_path):
            return []

        try:
            with open(self.json_path, "r", encoding="utf-8") as db_file:
                content = db_file.read().strip()
                if not content:
                    return []
                db_file.seek(0)
                return json.load(db_file)
        except (json.JSONDecodeError, Exception):
            # Si está corrupto, regresamos lista vacía
            return []

    def __save_data(self, data: List[Dict[str, Any]]) -> None:
        with open(self.json_path, "w", encoding="utf-8") as db_file:
            json.dump(data, db_file, indent=4, ensure_ascii=False)

    # ----------------- CRUD -----------------

    def add_record(self, record: Dict[str, Any]) -> None:
        """Agrega un registro al JSON."""
        data = self.__load_data()
        if "timestamp" not in record:
            record["timestamp"] = datetime.now().isoformat()
        data.append(record)
        self.__save_data(data)

    def get_record(self, file_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un registro por id (soporta 'id' o 'file_id')."""
        data = self.__load_data()
        for entry in data:
            current_id = entry.get("id") or entry.get("file_id")
            if current_id == file_id:
                return entry
        return None

    def update_record(self, file_id: str, updates: Dict[str, Any]) -> bool:
        """Actualiza campos de un registro identificado por id."""
        data = self.__load_data()
        for entry in data:
            current_id = entry.get("id") or entry.get("file_id")
            if current_id == file_id:
                entry.update(updates)
                self.__save_data(data)
                return True
        return False

    def list_records(self) -> List[Dict[str, Any]]:
        """Regresa todos los registros del JSON."""
        return self.__load_data()

    def delete_record(self, file_id: str) -> bool:
        """Elimina un registro por id."""
        data = self.__load_data()
        new_data = [
            entry for entry in data
            if (entry.get("id") or entry.get("file_id")) != file_id
        ]

        if len(new_data) != len(data):
            self.__save_data(new_data)
            return True
        return False

    def delete_all(self) -> None:
        """Elimina todos los registros (para la ruta /clear)."""
        self.__save_data([])
