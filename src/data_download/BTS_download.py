import os
import requests
import zipfile
from io import BytesIO
from datetime import date

def download_bts_data(start_year, start_month, end_year, end_month, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    year = start_year
    month = start_month

    while (year < end_year) or (year == end_year and month <= end_month):
        url = f"https://transtats.bts.gov/PREZIP/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_{year}_{month}.zip"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"can not find data for {year}-{month:02d}")
        else:
            # Unzipping
            with zipfile.ZipFile(BytesIO(response.content)) as z:
                for name in z.namelist():
                    # There are two file in each zipfile, a csv file and a readme html file
                    if name.endswith(".csv"):
                        # Create output file name
                        new_name = f"[{year}-{month:02d}]On_Time_Reporting.csv"
                        output_path = os.path.join(output_folder, new_name)

                        # Extract CSV and rename it
                        with z.open(name) as csv_file, open(output_path, "wb") as out_file:
                            out_file.write(csv_file.read())

                        print(f"Saved {output_path}")
                        break
                else:
                    print(f"No csv found inside the zipfile for {year}-{month:02d}")

        # Go to the next month
        month += 1
        if month > 12:
            month = 1
            year += 1

    print("\n Finished")


download_bts_data(
    start_year=2023,
    start_month=1,
    end_year=2023,
    end_month=3,
    output_folder="../data" # Probably need to change this to a full path, something wrong with this path
)
