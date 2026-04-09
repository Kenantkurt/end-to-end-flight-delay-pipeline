SELECT
    DATE(flight_date) AS flight_date,
    airline_code,
    flight_number,
    origin_airport_id,
    destination_airport_id,
    departure_delay,
    arrival_delay,
    is_cancelled,
    cancellation_code,
    is_diverted,
    carrier_delay,
    weather_delay,
    nas_delay,
    security_delay,
    late_aircraft_delay

FROM {{ source('flight_data', 'flight_delays') }}