# When bike rentals peak

Public-data learning study | Prepared with assistance

Question: should an operations team plan around one average rental pattern, or separate working days from weekends and holidays?

This is a descriptive study of Capital Bikeshare's 2011-2012 hourly and daily records. It is not current demand, a station-level staffing plan, or a prediction model. The files and findings are real; no workplace results or unaided coding claims are made.

![Hourly demand](hourly-demand.png)

## Findings

- Working-day rentals peak at 17:00: 262,120 rentals / 499 observed hours = 525.3 per hour. The morning 08:00 mean is 477.0 across 496 observed hours.
- Weekends and holidays peak at 13:00: 86,101 rentals / 231 observed hours = 372.7 per hour. These days are a different group, not just a lower copy of the working-day curve.
- Registered rentals account for 2,672,662 / 3,292,679 rentals (81.2%). Rentals are events, not unique people.
- There are no null cells, but 165 / 17,544 possible calendar-hour records (0.94%) are absent. Missing records must not be quietly turned into observed zero demand.

The practical hypothesis is to test different rebalancing windows by day type. Before acting, a team would need current station-level stock, capacity, availability and trip directions. These totals cannot identify which stations need bikes or prove a service improvement.

## Run

Python 3.10+; tested with Python 3.10.12, pandas 2.3.3 and matplotlib 3.10.9.

```sh
python -m pip install -r requirements.txt
python analyze.py
```

The original CSVs are included in this repository. The script regenerates the chart, aggregate CSVs and `outputs/results.json`. It checks row counts, unique date/ID keys, no nulls, `casual + registered = cnt`, and each day's hourly totals against `day.csv`. Output SHA256 hashes record the exact raw CSV inputs. Change the data only if the checks and source notes are updated.

## Method and limits

Each point is the sum of rentals divided by the number of observed records for that hour and day type. A missing hour is not imputed. `workingday=1` means neither weekend nor holiday in the supplied data. Both years are pooled; growth, seasons, weather and holiday mix can affect comparisons. The 2012 daily mean is 5,599.9 across 366 days, versus 3,405.8 across 365 days in 2011. That change is descriptive, not evidence for its cause.

Weather averages are exported for exploration, not presented as causal effects. Weather category 4 has just three records and is too small for a strong comparison. `casual` and `registered` must never be inputs to a model predicting `cnt` because their sum is the target. No model is fitted here.

## Attribution

Hadi Fanaee-T, *Bike Sharing*, UCI Machine Learning Repository, DOI 10.24432/C5W894. Source page lists CC BY 4.0. Analysis and charts are new transformations; original data and supplied Readme.txt are unchanged.

- Dataset and license: https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset
- Exact download: https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip
- Associated paper: Fanaee-T, Hadi and Gama, Joao (2013), *Event labeling combining ensemble detectors and background knowledge*. DOI 10.1007/s13748-013-0040-3, cited as requested by the supplied Readme.

Data accessed 1 October 2026. Source license applies to the dataset; no separate code license is selected for this project.
