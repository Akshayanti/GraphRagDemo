import glob
import json
import os
from typing import List, Dict
from langchain.schema import Document


class CVEDataProcessor:
    def __init__(self, output_directory: str):
        self.graph_documents = []
        self.documents = []
        self.output_directory = output_directory

    def load_json_files(self) -> None:
        json_files = glob.glob(os.path.join(self.output_directory, "*.json"))
        for json_file in json_files:
            with open(json_file, "r") as file:
                data = json.load(file)
                self.documents.append(data)

    def transform_to_graph_documents(self) -> None:
        for doc in self.documents:
            for cve in doc.get("CVEs", []):
                cve_id = cve.get("cve_id", "")
                description = (
                    cve.get("description", "").replace("\n", " ").replace("\r", " ")
                )
                impact = cve.get("impact_score", "")
                published_date = cve.get("published_date", "")
                assigner = cve.get("assigner", "")
                problemtype_descriptions = cve.get("problemtype_descriptions", [])
                metadata = {
                    "id": cve_id,
                    "Description": description,
                    "Impact": impact,
                    "PublishedDate": published_date,
                    "Assigner": assigner,
                    "ProblemType": problemtype_descriptions,
                }
                graph_document = Document(page_content=description, metadata=metadata)
                self.graph_documents.append(graph_document)

    def process(self) -> List[Document]:
        self.load_json_files()
        self.transform_to_graph_documents()
        return self.graph_documents
