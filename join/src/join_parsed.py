from pathlib import Path
import pandas as pd
from pyprojroot.here import here
import json
import dateparser


def year_or_none(date_str):
    try:
        return dateparser.parse(date_str).year
    except (TypeError, AttributeError):
        return None

parsed_fn_paths = Path(here("parse/output/")).glob("*.json")
jsons = []
for path in parsed_fn_paths:
    with open(path) as f:
        jsons.append(json.load(f))


degrees = []
employment = []
visits = []
honors = []
parents = []
people = []

person_keys = ['full_name', 'birthdate', 'deathdate', 'birthplace']

for js in jsons:
    birthyear = year_or_none(js['birthdate'])
    deathyear = year_or_none(js['deathdate'])

    personal = {k: js[k] for k in person_keys}
    personal['birthyear'] = birthyear
    personal['deathyear'] = deathyear
    people.append(personal)
    degrees.extend([{**deg, **personal} for deg in js['degrees']])
    employment.extend({**emp, **personal} for emp in js['employment'])
    visits.extend({**vis, **personal} for vis in js['visits'])
    honors.extend({**hon, **personal} for hon in js['honors'])
    parents.extend({
        'parent_name': p['name'],
        'parent_birthdate': p['birthdate'],
        'parent_deathdate': p['deathdate'],
        'parent_birthyear': year_or_none(p['birthdate'] or ''),
        'parent_deathyear': year_or_none(p['deathdate'] or ''),
        'parent_profession': p['profession'], **personal} for p in js['parents'])

df_people = pd.DataFrame(people)
df_degrees = pd.DataFrame(degrees)
df_employment = pd.DataFrame(employment)
df_visits = pd.DataFrame(visits)
df_honors = pd.DataFrame(honors)
df_parents = pd.DataFrame(parents)

df_people.to_csv(here("join/output/personal.csv"), index=False)
df_degrees.to_csv(here("join/output/degrees.csv"), index=False)
df_employment.to_csv(here("join/output/employment.csv"), index=False)
df_visits.to_csv(here("join/output/visits.csv"), index=False)
df_honors.to_csv(here("join/output/honors.csv"), index=False)
df_parents.to_csv(here("join/output/parents.csv"), index=False)
