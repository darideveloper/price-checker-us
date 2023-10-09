
CREATE TABLE `Status` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255)
);

CREATE TABLE `LogsType` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255)
);

CREATE TABLE `Logs` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `log_type` integer,
  `id_store` integer,
  `id_request` integer,
  `api_key` integer,
  `message` varchar(255)
);

ALTER TABLE `Products` ADD FOREIGN KEY (`id_store`) REFERENCES `Stores` (`id`);

ALTER TABLE `Products` ADD FOREIGN KEY (`id_request`) REFERENCES `Requests` (`id`);

ALTER TABLE `Requests` ADD FOREIGN KEY (`status`) REFERENCES `Status` (`id`);

ALTER TABLE `Requests` ADD FOREIGN KEY (`api_key`) REFERENCES `ApiKeys` (`id`);

ALTER TABLE `Logs` ADD FOREIGN KEY (`log_type`) REFERENCES `LogsType` (`id`);

ALTER TABLE `Logs` ADD FOREIGN KEY (`id_store`) REFERENCES `Stores` (`id`);

ALTER TABLE `Logs` ADD FOREIGN KEY (`id_request`) REFERENCES `Requests` (`id`);

ALTER TABLE `Logs` ADD FOREIGN KEY (`api_key`) REFERENCES `ApiKeys` (`id`);
