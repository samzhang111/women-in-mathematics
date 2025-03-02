import json
from pathlib import Path

from pyprojroot.here import here
from openai import OpenAI

import json_repair
from openai_key import OPENAI_KEY

client = OpenAI(api_key=OPENAI_KEY)

def query_chatgpt_and_save(bio_text, output_filename):
    """
    Queries the OpenAI ChatGPT API with a biographical summary and saves the response in JSON format.

    :param bio_text: The biographical summary to be processed.
    :param api_key: The OpenAI API key for authentication.
    :param output_filename: The filename where the response JSON will be saved.
    """

    prompt = f"""Given the following biographical summary, return the following data in JSON format:
- full_name
- birthdate
- deathdate
- birthplace
- parents: [List of Parents]
- employment: [List of Employment]
- degrees: [List of Degrees]
- visits: [List of Visits]
- honors: [List of Honors]

where each Parent is a JSON object with keys
- name
- birthdate
- deathdate
- profession

Employment is a JSON object with keys
- employer
- job_title
- job_year_begin
- job_year_end
- reason_end

Degree is a JSON object with keys
- degree_institution_name
- degree_type (eg: BA, MA, PhD)
- degree_year
- degree_advisor

Visit is a JSON object with keys:
- visit_location
- visit_reason
- visit_year

Honors is a JSON object with keys:
- honor_name
- honor_year

---
{bio_text}"""

    output_path = Path(here("parse/output/")) / output_filename

    try:
        response = client.chat.completions.create(model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI that extracts structured data from text, returning a JSON object and no other text."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3)


        json_response = response.choices[0].message.content
        parsed_response = json_repair.loads(json_response)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(parsed_response, f, indent=4)

        print(f"Response saved to {output_path}")
    except Exception as e:
        print(f"Error: {e}. Writing raw data.")

        with open(output_path, "w") as out:
            out.write(response.choices[0].message.content)

for fn_bio in Path(here("extract/output/")).glob("*.txt"):
    new_name = fn_bio.name.split('.')[0] + '.json'
    print(new_name)
    with open(fn_bio) as f:
        bio = f.read()

    query_chatgpt_and_save(bio, new_name)
