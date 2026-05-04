# WhoScored Pipeline

This module contains the WhoScored data pipeline used to collect, organize, and prepare match event data for football analysis.

The pipeline is currently focused on extracting match events from selected leagues and seasons, storing the raw data, cleaning it, and exporting it into a usable format for analysis and visualization.

---

## Purpose

The goal of this pipeline is to make it easier to collect match-level event data from WhoScored for leagues beyond the usual public datasets.

This is especially useful for scouting and analysis in competitions where structured event data is harder to access, such as smaller European leagues, South American leagues, US leagues, and lower divisions when available.

---

## Current Features

- Extracts fixture and match information for a selected country, league, and season
- Identifies matches that have already been played
- Collects match event data from played match pages
- Stores raw match data in JSON format
- Loads saved match events into a dataframe
- Normalizes the event data into a cleaner structure
- Maps team identifiers to team names
- Exports cleaned match event data to CSV

---

## Data Flow

The pipeline follows this general flow:

1. Select country, league, and season
2. Collect fixture and match URLs
3. Filter played matches
4. Extract match event data
5. Store raw data
6. Normalize events
7. Export cleaned data

---

## Output

The pipeline produces two main types of output:

### Raw JSON

Stores the scraped match event data before transformation.  
This is useful for debugging, recovery, and reprocessing without scraping the same matches again.

### Clean CSV

Stores normalized match events in a dataframe-friendly format.  
This is the main output used for analysis, visualization, and future tools.

---

## Intended Use

The cleaned match event data can be used for:

- match analysis
- event-based visualizations
- player and team analysis
- scouting workflows
- tactical reports
- future data tools in this project

---

## Notes

This pipeline is intended for personal football analysis, scouting practice, and research.

When working with external data sources, usage should remain respectful of the source website, including request frequency, access limitations, and terms of use.

---

## Future Improvements

Planned improvements include:

- better error handling
- stronger resume/recovery logic
- additional event normalization
- automated validation of exported data
- integration with visualization and player profiling tools