from weather_etl.transform import main
import pandas as pd
import pytest


def test_transform_valid(temp_data_dir, monkeypatch):
    """Ensure extracted data processed successfully."""
    config_file = temp_data_dir.parent / "test_config.conf"
    monkeypatch.setenv("TEST_CONFIG", str(config_file))
    test_file_path = temp_data_dir / "weather_transformed.csv"
    input = """name,datetime,temp,feelslike,dew,humidity,precip,precipprob,preciptype,snow,snowdepth,windgust,windspeed,winddir,sealevelpressure,cloudcover,visibility,solarradiation,solarenergy,uvindex,severerisk,conditions,icon,stations
            مصر,2025-03-14T00:00:00,18.5,18.5,10.8,60.83,0.0,0.0,,0,0,3.6,2.5,20.3,1015.0,99.9,24.1,0.0,0.0,0,10,Overcast,cloudy,
            مصر,2025-03-14T01:00:00,17.7,17.7,11.2,65.69,0.0,0.0,,0,0,3.6,2.2,26.9,1015.0,100.0,24.1,0.0,0.0,0,10,Overcast,cloudy,
            مصر,2025-03-14T00:00:00,18.5,18.5,10.8,60.83,0.0,0.0,,0,0,3.6,2.5,20.3,1015.0,99.9,24.1,0.0,0.0,0,10,Overcast,cloudy,
            """

    raw_data_path = temp_data_dir / "weather.csv"
    with open(raw_data_path, 'w') as f:
        f.write(input)
    
    # Run the transformation on the raw data
    main()

    assert test_file_path.exists(), "weather_trasnformed data file was not created."

    # Read the transformed data
    df = pd.read_csv(test_file_path)
    columns_to_drop = ["stations", "preciptype"]
    for col in columns_to_drop:
        assert col not in df.columns, f"{columns_to_drop} didn't dropped from the df"
    
    assert df["name"].unique()[0].strip() == "Egypt", f"Name column not converted"
    assert "timestamp" in df.columns, "timestamp column not found"
    assert len(df) == 2, "Duplicates not dropped"