CREATE TABLE IF NOT EXISTS event (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    image_id VARCHAR(255),
    description TEXT
);

CREATE TABLE IF NOT EXISTS user_account (
    id VARCHAR(255) PRIMARY KEY,
    twitch_id VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS streamer (
    id VARCHAR(255) PRIMARY KEY,
    twitch_id VARCHAR(255) NOT NULL UNIQUE,
    `name` VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS additional_link (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id VARCHAR(255),
    url VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    FOREIGN KEY (event_id) REFERENCES event(id)
);

CREATE TABLE IF NOT EXISTS highlight (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id VARCHAR(255),
    `url` VARCHAR(2083) NOT NULL,
    author_id VARCHAR(255) NOT NULL,
    attached_datetime DATETIME NOT NULL,
    FOREIGN KEY (event_id) REFERENCES event(id),
    FOREIGN KEY (author_id) REFERENCES user_account(id)
);

CREATE TABLE IF NOT EXISTS participation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id VARCHAR(255),
    streamer_id VARCHAR(255),
    FOREIGN KEY (event_id) REFERENCES `event`(id),
    FOREIGN KEY (streamer_id) REFERENCES streamer(id)
);

CREATE TABLE IF NOT EXISTS event_role (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS account_event_access (
    id VARCHAR(255) PRIMARY KEY,
    account_id VARCHAR(255) NOT NULL,
    event_id VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES user_account(id),
    FOREIGN KEY (event_id) REFERENCES `event`(id),
    FOREIGN KEY (role_id) REFERENCES event_role(id)
);