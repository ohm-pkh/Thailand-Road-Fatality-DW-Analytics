CREATE TABLE IF NOT EXISTS warehouse.dim_location(
    id INT,
    subdistrict VARCHAR(100),
    district VARCHAR(100),
    province VARCHAR(100),
    subdistrict_th VARCHAR(100),
    district_th VARCHAR(100),
    province_th VARCHAR(100),
    province_shortname_th VARCHAR(2),
    province_lat float,
    province_lon float
);