# JSONL to Excel and Excel to JSONL Conversion

## Purpose

The primary purpose of the [script](https://github.com/gsk-tech/AIGA/blob/main/llmops/common/jsonl_converter.py) is to:

1. Enable users to easily convert JSONL data to a more user-friendly Excel format for sharing it with business users.
2. Allow users to convert Excel data back into JSONL format so that we can input the same for promptflow evaluation.

## Usage

1. Test Case Collection: The business provides the test cases in an Excel file.
2. Data Transformation: We transform the Excel file into a .jsonl file format.
3. Pipeline Application: The transformed .jsonl file is processed through the [prompt pipeline](https://github.com/gsk-tech/AIGA/blob/main/llmops/common/prompt_pipeline.py).
4. Output Generation: The pipeline generates an AI output, which is saved as ai-generated.csv in the report folder.
5. Business Review: The ai-generated.csv is shared with the business for review.
6. Feedback Integration: Once the business rates all entries as 4 or 5, we transform the ai-generated.csv back into a .jsonl file.
7. Golden Dataset Creation: The validated .jsonl file is incorporated into the Golden Dataset.

## Self-Usage and Integration

Users can also leverage the functions provided in this script. Here is how you can import and use these functions:

### Using the Script

To use the script as it is, user needs to setup the correct environment variables in the `.env` file and to run the script using the command mentioned below.

``` shell
poetry run python llmops/common/jsonl_converter.py
```

### Importing Functions

To use the conversion functions in your own scripts, you can import them as follows:

```python
from llmops.common.jsonl_converter import jsonl_to_excel, excel_to_jsonl, csv_to_jsonl
```

Please update the file paths either in `.env` and AI output column name before for running the script.

By importing these functions, you can easily integrate JSONL to Excel, Excel to JSONL, CSV to JSONL conversion capabilities into your own data processing pipelines.
