WITH weather_dedup AS (
    SELECT
        DATE(flight_date) AS flight_date,
        origin_airport_id,

        AVG(max_temperature_c) AS max_temperature_c,
        AVG(min_temperature_c) AS min_temperature_c,
        AVG(total_precipitation_mm) AS total_precipitation_mm,
        AVG(total_snowfall_mm) AS total_snowfall_mm,
        AVG(total_rain_mm) AS total_rain_mm

    FROM {{ ref('stg_weather') }}
    GROUP BY 1,2
)

SELECT
    f.flight_date,
    f.airline_code,
    f.flight_number,
    f.origin_airport_id,
    f.destination_airport_id,
    f.departure_delay,
    f.arrival_delay,
    f.is_cancelled,
    f.cancellation_code,
    f.is_diverted,
    f.carrier_delay,
    f.weather_delay,
    f.nas_delay,
    f.security_delay,
    f.late_aircraft_delay,

    w.max_temperature_c,
    w.min_temperature_c,
    w.total_precipitation_mm,
    w.total_snowfall_mm,
    w.total_rain_mm,

    h.holiday_name

FROM {{ ref('stg_flight_delays') }} f

LEFT JOIN weather_dedup w
    ON DATE(f.flight_date) = w.flight_date
    AND f.origin_airport_id = w.origin_airport_id

LEFT JOIN {{ ref('stg_holidays') }} h
    ON h.date = DATE(f.flight_date)