SELECT
    DATE(flight_date) AS flight_date,
    airline_code,
    flight_number,
    origin_airport_id,
    destination_airport_id,
    departure_delay,
    arrival_delay,
    carrier_delay,
    weather_delay,
    nas_delay,
    security_delay,
    late_aircraft_delay,
    max_temperature_c,
    min_temperature_c,
    total_precipitation_mm,
    total_snowfall_mm,
    total_rain_mm
FROM {{ source('flight_data', 'flight_weather') }}
