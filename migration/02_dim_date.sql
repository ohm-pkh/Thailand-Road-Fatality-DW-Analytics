CREATE TABLE IF NOT EXISTS warehouse.dim_date(
    id INT,
    date DATE,
    date_description VARCHAR(50),
    day_fullname VARCHAR(50),
    day_shortname VARCHAR(50),
    month_fullname VARCHAR(50),
    month_shortname VARCHAR(50),
    season VARCHAR(50),
    calendar_day INT,
    calendar_day_in_week INT,
    calendar_month INT,
    calendar_day_in_month INT,
    calendar_quarter INT,
    calendar_day_in_quatre INT,
    calendar_day_in_season INT,
    calendar_year INT,
    calendar_year_be INT
);