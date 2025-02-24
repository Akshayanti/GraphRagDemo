import glob
import json
import os

from tqdm import tqdm


class CVEDataFilter:
    def __init__(self, input_directory: str, output_directory: str):
        self.input_directory = input_directory
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)
        self.cve_ids = set()
        self.all_cve_ids = set()

    def filter_cve_data(self, input_path: str, output_path: str):
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)  # Load the JSON file

        # Extract relevant fields from each CVE entry
        filtered_items = []
        for item in data.get("CVE_Items", []):
            cve_id = item.get("cve", {}).get("CVE_data_meta", {}).get("ID", "Unknown")
            if cve_id != "Unknown":
                self.all_cve_ids.add(cve_id)
                if "2024" in input_path:
                    self.cve_ids.add(cve_id)
            description_data = (
                item.get("cve", {}).get("description", {}).get("description_data", [])
            )
            description = (
                description_data[0].get("value", "No description")
                if description_data
                else "No description"
            )
            impact = (
                item.get("impact", {})
                .get("baseMetricV3", {})
                .get("cvssV3", {})
                .get("baseScore", "N/A")
            )
            published_date = item.get("publishedDate", "Unknown")
            assigner = (
                item.get("cve", {}).get("CVE_data_meta", {}).get("ASSIGNER", "Unknown")
            )
            problemtype_data = (
                item.get("cve", {}).get("problemtype", {}).get("problemtype_data", [])
            )
            problemtype_descriptions = [
                ptype.get("description", [{}])[0].get("value", "Unknown")
                for ptype in problemtype_data
                if ptype.get("description")
            ]

            filtered_items.append(
                {
                    "cve_id": cve_id,
                    "description": description,
                    "impact_score": impact,
                    "published_date": published_date,
                    "assigner": assigner,
                    "problemtype_descriptions": problemtype_descriptions,
                }
            )

        out_data = {"CVEs": filtered_items}

        # Save the filtered data as a JSON file
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(out_data, f, indent=2)

    def filter_jsons(self):
        input_files = glob.glob(os.path.join(self.input_directory, "*.json"))
        for input_file in tqdm(input_files, desc="Compressing Original JSONs"):
            output_file = os.path.join(
                self.output_directory, f"compressed-{os.path.basename(input_file)}"
            )
            self.filter_cve_data(input_file, output_file)

    def get_latest_cve_ids(self):
        return self.cve_ids

    def get_all_cve_ids(self):
        return self.all_cve_ids
