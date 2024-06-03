-- Файл миграции для создания таблицы table_mfc_2

CREATE TABLE table_mfc_2 (
    id SERIAL PRIMARY KEY,
    session_topic TEXT,
    count_topic INT,
    date_session DATE
);
