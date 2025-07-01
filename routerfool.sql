SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `banos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `capacidad` int(11) NOT NULL,
  `en_uso` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `banos_log` (
  `id` int(11) NOT NULL,
  `id_visitante` int(11) DEFAULT NULL,
  `id_bano` int(11) DEFAULT NULL,
  `hora_entrada` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `compras_comida` (
  `id` int(11) NOT NULL,
  `id_visitante` int(11) DEFAULT NULL,
  `id_puesto` int(11) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `hora` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `juegos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `capacidad` int(11) NOT NULL,
  `en_uso` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `juegos_log` (
  `id` int(11) NOT NULL,
  `id_visitante` int(11) DEFAULT NULL,
  `id_juego` int(11) DEFAULT NULL,
  `hora_entrada` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `puestos_comida` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `stock` int(11) NOT NULL,
  `ventas` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `visitantes` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `edad` int(11) DEFAULT NULL,
  `hora_ingreso` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

ALTER TABLE `banos`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `banos_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_visitante` (`id_visitante`),
  ADD KEY `id_bano` (`id_bano`);

ALTER TABLE `compras_comida`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_visitante` (`id_visitante`),
  ADD KEY `id_puesto` (`id_puesto`);

ALTER TABLE `juegos`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `juegos_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_visitante` (`id_visitante`),
  ADD KEY `id_juego` (`id_juego`);

ALTER TABLE `puestos_comida`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `visitantes`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `banos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `banos_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `compras_comida`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `juegos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `juegos_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `puestos_comida`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `visitantes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `banos_log`
  ADD CONSTRAINT `banos_log_ibfk_1` FOREIGN KEY (`id_visitante`) REFERENCES `visitantes` (`id`),
  ADD CONSTRAINT `banos_log_ibfk_2` FOREIGN KEY (`id_bano`) REFERENCES `banos` (`id`);

ALTER TABLE `compras_comida`
  ADD CONSTRAINT `compras_comida_ibfk_1` FOREIGN KEY (`id_visitante`) REFERENCES `visitantes` (`id`),
  ADD CONSTRAINT `compras_comida_ibfk_2` FOREIGN KEY (`id_puesto`) REFERENCES `puestos_comida` (`id`);

ALTER TABLE `juegos_log`
  ADD CONSTRAINT `juegos_log_ibfk_1` FOREIGN KEY (`id_visitante`) REFERENCES `visitantes` (`id`),
  ADD CONSTRAINT `juegos_log_ibfk_2` FOREIGN KEY (`id_juego`) REFERENCES `juegos` (`id`);

COMMIT;
