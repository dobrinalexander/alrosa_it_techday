CREATE SCHEMA IF NOT EXISTS core_data;

DROP TABLE IF EXISTS core_data.content_table;

CREATE TABLE IF NOT EXISTS core_data.content_table(
    id VARCHAR(100) PRIMARY KEY
    ,ticker VARCHAR(40) NOT NULL
    ,inserted TIMESTAMP NOT NULL
    ,price FLOAT NOT NULL
    ,nickname VARCHAR(100) NOT NULL
    ,likesCount int NOT NULL
    ,content VARCHAR(1000000) NOT NULL
    ,max_cursor INT NOT NULL
);

CREATE TABLE IF NOT EXISTS core_data.count_content_by_user(
    nickname VARCHAR(100) NOT NULL
    ,cnt_content int NOT NULL
)

SELECT * FROM core_data.content_table;