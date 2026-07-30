-- ============================================================
-- status_types: Kategorik hava durumu özetlerini tutan lookup tablo
-- ============================================================
CREATE TABLE IF NOT EXISTS status_types (
    status_id INT PRIMARY KEY,
    summary VARCHAR(100),
    precip_type VARCHAR(50)
);

-- ============================================================
-- weather_data: Ana ölçüm tablosu
-- ============================================================
CREATE TABLE IF NOT EXISTS weather_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    formatted_date DATETIME,
    temperature_c FLOAT,
    apparent_temperature_c FLOAT,
    humidity FLOAT,
    wind_speed_kmh FLOAT,
    wind_bearing_degrees FLOAT,
    visibility_km FLOAT,
    pressure_millibars FLOAT,
    daily_summary TEXT,
    year INT,
    month INT,
    day INT,
    status_id INT
);

-- ============================================================
-- Foreign Key: weather_data.status_id -> status_types.status_id
-- ============================================================
ALTER TABLE weather_data
ADD CONSTRAINT fk_weather_status
FOREIGN KEY (status_id) REFERENCES status_types(status_id);
