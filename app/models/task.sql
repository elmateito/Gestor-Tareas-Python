-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-05-2024 a las 06:16:03
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `task`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tareas`
--

CREATE TABLE `tareas` (
  `idTarea` int(11) NOT NULL,
  `nombreTarea` varchar(200) NOT NULL,
  `fechaInicio` date NOT NULL,
  `fechaFin` date NOT NULL,
  `estado` varchar(20) NOT NULL,
  `idUsuarioFK` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tareas`
--

INSERT INTO `tareas` (`idTarea`, `nombreTarea`, `fechaInicio`, `fechaFin`, `estado`, `idUsuarioFK`) VALUES
(42, 'test', '2023-06-21', '2023-09-14', 'Por Definir', 17),
(43, 'test2', '2024-05-09', '2024-05-09', 'Por Definir', 18);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `idUsuario` int(11) NOT NULL,
  `nombre` varchar(128) NOT NULL,
  `apellido` varchar(128) NOT NULL,
  `correo` varchar(128) NOT NULL,
  `nombreUsuario` varchar(128) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `rol` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`idUsuario`, `nombre`, `apellido`, `correo`, `nombreUsuario`, `contraseña`, `rol`) VALUES
(15, 'usuario', 'usuario', 'usuario@usuario.com', 'usuario', 'scrypt:32768:8:1$vwLhTEhcqjKQSfV6$b006cda865fa1af0100ef96c1ce38c122242c50fb136cadd1974e41c75c332a220dc97901958daa3ceba5eb43ddb81ac7ec7e9d9a9a1893ccd2ef0ec7b0aee8c', 'Usuario'),
(17, 'admin', 'admin', 'admin@admin', 'admin', 'scrypt:32768:8:1$6fGPm018n7Vtp3X3$d2ccf73065b31e571125989040989dc27e9a7bc47fa6a51d7e7c0869357a93a6fde1faf6e4cbd6f7e4c7cc6146c980b7532303de15582255b47ae9d6673c4751', 'Administrador'),
(18, 'admin2', 'admin2', 'admin@admin.com', 'admin2', 'scrypt:32768:8:1$oPstubtejz4mMyGZ$fec5fc96b1b884c59847f3a3527ca986ae4095af7a9000caf15394caf7aca97234837398fd7e7d0be6160473989d9ba437ac45b402d950a1b5d8e797227062ac', 'Administrador');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `tareas`
--
ALTER TABLE `tareas`
  ADD PRIMARY KEY (`idTarea`),
  ADD KEY `idUsuarioFK` (`idUsuarioFK`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`idUsuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `tareas`
--
ALTER TABLE `tareas`
  MODIFY `idTarea` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `idUsuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `tareas`
--
ALTER TABLE `tareas`
  ADD CONSTRAINT `tareas_ibfk_1` FOREIGN KEY (`idUsuarioFK`) REFERENCES `usuarios` (`idUsuario`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
