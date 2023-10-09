CREATE TABLE `log_types` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255)
);

CREATE TABLE `log_origins` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255)
);

CREATE TABLE `Logs` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `id_log_type` integer,
  `id_log_origin` integer,
  `id_store` integer,
  `id_request` integer,
  `id_api_key` integer,
  `message` varchar(255)
);

ALTER TABLE `Logs` ADD FOREIGN KEY (`id_log_type`) REFERENCES `log_types` (`id`);

ALTER TABLE `Logs` ADD FOREIGN KEY (`id_log_origin`) REFERENCES `log_origins` (`id`);

ALTER TABLE `Logs` ADD FOREIGN KEY (`id_store`) REFERENCES `Stores` (`id`);

ALTER TABLE `Logs` ADD FOREIGN KEY (`id_request`) REFERENCES `Requests` (`id`);

ALTER TABLE `Logs` ADD FOREIGN KEY (`id_api_key`) REFERENCES `ApiKeys` (`id`);
