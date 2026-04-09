SELECT *
FROM {{ source('flight_data', 'airports') }}