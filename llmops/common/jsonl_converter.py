import json
import os
import pandas as pd
from dotenv import load_dotenv

# Please add the coumn / output variable name from your promptflow here.
AI_OUTPUT_COLUMNNAME = "answer"

load_dotenv()
# Add jsonl and excel file path in env.yaml with their extension mentioned in path.
jsonl_path = os.getenv("JSON_FILE_PATH")
excel_path = os.getenv("EXCEL_FILE_PATH")
csv_path = os.getenv("CSV_FILE_PATH")


def jsonl_to_excel(jsonl_path=jsonl_path):
    try:
        with open(jsonl_path, "r", encoding="utf-8") as f:
            data = [json.loads(line) for line in f]
        df = pd.DataFrame(data)
    except Exception as e:
        print(f"Error occured reading JSONL : {e}")
    else:
        output_path = jsonl_path.replace("jsonl", "xlsx")
        df = df.rename(columns={AI_OUTPUT_COLUMNNAME: "Groundtruth"})
        # Add empty column for business to grade
        df["Grade"] = ""
        df.to_excel(output_path, index=False)


def excel_to_jsonl(excel_path=excel_path):
    data = pd.read_excel(excel_path)
    output_path = excel_path.replace("xlsx", "jsonl")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(data.to_json(orient="records", lines=True, force_ascii=False))
    except Exception as e:
        print(f"Failed to convert to JSONL : {e}")


def csv_to_jsonl(csv_path=csv_path):
    data = pd.read_csv(csv_path)
    output_path = csv_path.replace("csv", "jsonl")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(data.to_json(orient="records", lines=True, force_ascii=False))
    except Exception as e:
        print(f"Failed to convert to JSONL : {e}")


if __name__ == "__main__":
    jsonl_to_excel()
    excel_to_jsonl()
