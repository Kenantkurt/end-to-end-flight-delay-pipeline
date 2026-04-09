SELECT *
FROM {{ source('flight_data', 'airlines') }}
