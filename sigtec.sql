-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 21/10/2026 às 19:38
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `sigtec`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `arquivo`
--

CREATE TABLE `arquivo` (
  `id` int(11) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `descricao` varchar(255) NOT NULL,
  `arquivo` varchar(100) NOT NULL,
  `id_pessoa` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Despejando dados para a tabela `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 3, 'add_permission'),
(6, 'Can change permission', 3, 'change_permission'),
(7, 'Can delete permission', 3, 'delete_permission'),
(8, 'Can view permission', 3, 'view_permission'),
(9, 'Can add group', 2, 'add_group'),
(10, 'Can change group', 2, 'change_group'),
(11, 'Can delete group', 2, 'delete_group'),
(12, 'Can view group', 2, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add cargo', 8, 'add_cargo'),
(26, 'Can change cargo', 8, 'change_cargo'),
(27, 'Can delete cargo', 8, 'delete_cargo'),
(28, 'Can view cargo', 8, 'view_cargo'),
(29, 'Can add carreira', 9, 'add_carreira'),
(30, 'Can change carreira', 9, 'change_carreira'),
(31, 'Can delete carreira', 9, 'delete_carreira'),
(32, 'Can view carreira', 9, 'view_carreira'),
(33, 'Can add Nível de Acesso', 13, 'add_nivelacesso'),
(34, 'Can change Nível de Acesso', 13, 'change_nivelacesso'),
(35, 'Can delete Nível de Acesso', 13, 'delete_nivelacesso'),
(36, 'Can view Nível de Acesso', 13, 'view_nivelacesso'),
(37, 'Can add Situação', 18, 'add_situacao'),
(38, 'Can change Situação', 18, 'change_situacao'),
(39, 'Can delete Situação', 18, 'delete_situacao'),
(40, 'Can view Situação', 18, 'view_situacao'),
(41, 'Can add pessoa', 14, 'add_pessoa'),
(42, 'Can change pessoa', 14, 'change_pessoa'),
(43, 'Can delete pessoa', 14, 'delete_pessoa'),
(44, 'Can view pessoa', 14, 'view_pessoa'),
(45, 'Can add Log de Auditoria', 12, 'add_logauditoria'),
(46, 'Can change Log de Auditoria', 12, 'change_logauditoria'),
(47, 'Can delete Log de Auditoria', 12, 'delete_logauditoria'),
(48, 'Can view Log de Auditoria', 12, 'view_logauditoria'),
(49, 'Can add evento', 11, 'add_evento'),
(50, 'Can change evento', 11, 'change_evento'),
(51, 'Can delete evento', 11, 'delete_evento'),
(52, 'Can view evento', 11, 'view_evento'),
(53, 'Can add Dado Estatístico', 10, 'add_dadoestatistico'),
(54, 'Can change Dado Estatístico', 10, 'change_dadoestatistico'),
(55, 'Can delete Dado Estatístico', 10, 'delete_dadoestatistico'),
(56, 'Can view Dado Estatístico', 10, 'view_dadoestatistico'),
(57, 'Can add arquivo', 7, 'add_arquivo'),
(58, 'Can change arquivo', 7, 'change_arquivo'),
(59, 'Can delete arquivo', 7, 'delete_arquivo'),
(60, 'Can view arquivo', 7, 'view_arquivo'),
(61, 'Can add Cargo da Pessoa', 15, 'add_pessoacargo'),
(62, 'Can change Cargo da Pessoa', 15, 'change_pessoacargo'),
(63, 'Can delete Cargo da Pessoa', 15, 'delete_pessoacargo'),
(64, 'Can view Cargo da Pessoa', 15, 'view_pessoacargo'),
(65, 'Can add Histórico de Situação', 16, 'add_pessoasituacaohistorico'),
(66, 'Can change Histórico de Situação', 16, 'change_pessoasituacaohistorico'),
(67, 'Can delete Histórico de Situação', 16, 'delete_pessoasituacaohistorico'),
(68, 'Can view Histórico de Situação', 16, 'view_pessoasituacaohistorico'),
(69, 'Can add unidade', 19, 'add_unidade'),
(70, 'Can change unidade', 19, 'change_unidade'),
(71, 'Can delete unidade', 19, 'delete_unidade'),
(72, 'Can view unidade', 19, 'view_unidade'),
(73, 'Can add Unidade da Pessoa', 17, 'add_pessoaunidade'),
(74, 'Can change Unidade da Pessoa', 17, 'change_pessoaunidade'),
(75, 'Can delete Unidade da Pessoa', 17, 'delete_pessoaunidade'),
(76, 'Can view Unidade da Pessoa', 17, 'view_pessoaunidade');

-- --------------------------------------------------------

--
-- Estrutura para tabela `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `cargo`
--

CREATE TABLE `cargo` (
  `id` int(11) NOT NULL,
  `descricao` varchar(100) NOT NULL,
  `nivel` varchar(100) DEFAULT NULL,
  `siape` varchar(50) DEFAULT NULL,
  `cargo` varchar(100) NOT NULL,
  `padrao` varchar(50) DEFAULT NULL,
  `deletado` tinyint(1) NOT NULL DEFAULT 0
) ;

-- --------------------------------------------------------

--
-- Estrutura para tabela `carreira`
--

CREATE TABLE `carreira` (
  `id` int(11) NOT NULL,
  `descricao` varchar(100) NOT NULL,
  `deletado` tinyint(1) NOT NULL DEFAULT 0
) ;

--
-- Despejando dados para a tabela `carreira`
--

INSERT INTO `carreira` (`id`, `descricao`, `deletado`) VALUES
(1, 'Carreira de Ciência e Tecnologia', 0),
(2, 'Carreira de Gestão e Infraestrutura', 0),
(3, 'Plano Especial de Cargos', 0),
(4, 'Colaborador Terceirizado', 0),
(5, 'Bolsista', 0),
(6, 'Estagiário', 0);

-- --------------------------------------------------------

--
-- Estrutura para tabela `dado_estatistico`
--

CREATE TABLE `dado_estatistico` (
  `id` int(11) NOT NULL,
  `categoria` varchar(100) NOT NULL,
  `indicador` varchar(200) NOT NULL,
  `valor` decimal(12,2) NOT NULL,
  `periodo` varchar(50) NOT NULL,
  `observacao` longtext NOT NULL,
  `id_pessoa` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Despejando dados para a tabela `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'group'),
(3, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(7, 'pessoas', 'arquivo'),
(8, 'pessoas', 'cargo'),
(9, 'pessoas', 'carreira'),
(10, 'pessoas', 'dadoestatistico'),
(11, 'pessoas', 'evento'),
(12, 'pessoas', 'logauditoria'),
(13, 'pessoas', 'nivelacesso'),
(14, 'pessoas', 'pessoa'),
(15, 'pessoas', 'pessoacargo'),
(16, 'pessoas', 'pessoasituacaohistorico'),
(17, 'pessoas', 'pessoaunidade'),
(18, 'pessoas', 'situacao'),
(19, 'pessoas', 'unidade'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Estrutura para tabela `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Despejando dados para a tabela `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-10-20 17:37:33.800812'),
(2, 'auth', '0001_initial', '2026-10-20 17:37:34.167409'),
(3, 'admin', '0001_initial', '2026-10-20 17:37:34.253632'),
(4, 'admin', '0002_logentry_remove_auto_add', '2026-10-20 17:37:34.258371'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2026-10-20 17:37:34.262682'),
(6, 'contenttypes', '0002_remove_content_type_name', '2026-10-20 17:37:34.305549'),
(7, 'auth', '0002_alter_permission_name_max_length', '2026-10-20 17:37:34.584080'),
(8, 'auth', '0003_alter_user_email_max_length', '2026-10-20 17:37:34.592919'),
(9, 'auth', '0004_alter_user_username_opts', '2026-10-20 17:37:34.597833'),
(10, 'auth', '0005_alter_user_last_login_null', '2026-10-20 17:37:34.639019'),
(11, 'auth', '0006_require_contenttypes_0002', '2026-10-20 17:37:34.640001'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2026-10-20 17:37:34.644835'),
(13, 'auth', '0008_alter_user_username_max_length', '2026-10-20 17:37:34.653557'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2026-10-20 17:37:34.661105'),
(15, 'auth', '0010_alter_group_name_max_length', '2026-10-20 17:37:34.671426'),
(16, 'auth', '0011_update_proxy_permissions', '2026-10-20 17:37:34.675987'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2026-10-20 17:37:34.683504'),
(19, 'sessions', '0001_initial', '2026-10-20 17:38:14.285440'),
(20, 'pessoas', '0001_initial', '2026-10-20 17:40:22.368802');

-- --------------------------------------------------------

--
-- Estrutura para tabela `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Despejando dados para a tabela `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('0wqwnj84gy9rjrw8y0qstn61nnc30iym', 'e30:1xJa6x:XKN5S_vzdaejhPZSExJgBk7hrseV59nLyLNT5nTNE3w', '2026-11-04 17:28:23.309509'),
('bto4s6k5z4hb4ib9rvrkuf6ywd9gs8m7', 'eyJwZXNzb2FfaWQiOjF9:1xJZzY:ZhHjG-YssqAi4TIhILyP62lo8aZ2W5ERMPE9triD2Q4', '2026-11-04 17:20:44.312897'),
('fvh3s64kkwgoggptrarklcv3o8ufhnlz', 'eyJwZXNzb2FfaWQiOjF9:1xJDuG:dhU1QyO52nAMtJwfDzYybZnNNpa2hE2SUeFeP7qTxdU', '2026-11-03 17:45:48.957299'),
('g4lzywdmzgdq12jtxkojm8mosbgkggl9', 'eyJwZXNzb2FfaWQiOjF9:1xJZdR:YvMoj0Q283Yh85ifyAZbXM_aM80PJzKLJUwnxkqZeuM', '2026-11-04 16:57:53.787018'),
('igak4v0f1dy1kplm6m2ultncm5yw2m4z', 'eyJwZXNzb2FfaWQiOjJ9:1xJa8X:GziZbQ8MSR9DF-P6G5H84yF7AKY4DN02gNyV_7bTzeo', '2026-11-04 17:30:01.245654'),
('j9hogrouwj2g2z6zjd1ppskw7ei3wvre', 'eyJwZXNzb2FfaWQiOjF9:1xJaC9:l9o3C_eQvqXLeNfD5xf6duoLhAbAJ1dX_zUh4-SjLMk', '2026-11-04 17:33:45.463662'),
('kkmxdo1a0c2cdpuicxpnh8ye0253sul3', 'eyJwZXNzb2FfaWQiOjJ9:1xJa8Y:fPQ_rcudJ0Za2SChEAUohJNiQtvVXWVKhc9-0XjN4Dg', '2026-11-04 17:30:02.017071'),
('n30trsqyeiol243e8qsuvb2lmgkvka69', 'eyJwZXNzb2FfaWQiOjJ9:1xJZei:CUxKi3uxQqXS5wLcxBw7C15qYvrFChZxfclrEqgCIYo', '2026-11-04 16:59:12.161508'),
('q0ah09tz7kbq7pzzfew1ajqr8z26mls7', 'eyJwZXNzb2FfaWQiOjJ9:1xJa0q:-QmjvGWfdq2Zq459DP3tHCvlEJbk_CRWmbKZ71fBBEk', '2026-11-04 17:22:04.425454'),
('xuj7yd9l5dtmnodmoqeggyercd0zx6tx', 'eyJwZXNzb2FfaWQiOjF9:1xJa8Y:VRz7U_RZpX-nCfJYIT4P5DmJmd08Anr5vJIasaYOLow', '2026-11-04 17:30:02.000259');

-- --------------------------------------------------------

--
-- Estrutura para tabela `evento`
--

CREATE TABLE `evento` (
  `id` int(11) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `descricao` longtext NOT NULL,
  `dt_inicio` datetime(6) NOT NULL,
  `dt_fim` datetime(6) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `geral` tinyint(1) NOT NULL,
  `id_pessoa` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `log_auditoria`
--

CREATE TABLE `log_auditoria` (
  `id` bigint(20) NOT NULL,
  `id_pessoa` int(11) DEFAULT NULL COMMENT 'Quem executou a ação',
  `tabela` varchar(64) NOT NULL,
  `id_registro` varchar(64) NOT NULL,
  `acao` varchar(10) NOT NULL,
  `dados_anteriores` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`dados_anteriores`)),
  `dados_novos` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`dados_novos`)),
  `ip` varchar(45) DEFAULT NULL,
  `dt_evento` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Auditoria de ações no sistema';

--
-- Despejando dados para a tabela `log_auditoria`
--

INSERT INTO `log_auditoria` (`id`, `id_pessoa`, `tabela`, `id_registro`, `acao`, `dados_anteriores`, `dados_novos`, `ip`, `dt_evento`) VALUES
(4, 2, 'pessoa', '1', 'edicao', '{\"nome\": \"Usuario de Teste SIGTEC\", \"login\": \"teste.sigtec\", \"email\": \"teste.sigtec@example.invalid\", \"matricula\": \"TESTE-SIGTEC\"}', '{\"login\": \"teste.sigtec\", \"nome\": \"Usuario de Teste SIGTEC\", \"dt_nascimento\": \"2006-02-21\", \"dt_admissao\": \"2026-10-21\", \"dt_demissao\": null, \"matricula\": \"TESTE-SIGTEC\", \"cpf\": \"000.000.000-00\", \"id_situacao\": 1, \"id_carreira\": null, \"escolaridade\": null, \"titulacao\": null, \"id_responsavel\": null, \"cep\": null, \"logradouro\": null, \"complemento\": null, \"bairro\": null, \"cidade\": null, \"estado\": null, \"telefone\": null, \"email\": \"teste.sigtec@example.invalid\", \"genero\": null, \"nivel_acesso\": 3}', '127.0.0.1', '2026-10-21 20:08:07'),
(5, 2, 'pessoa', '3', 'edicao', '{\"nome\": \"Daniel de Souza Freitas\", \"login\": \"dfreitas\", \"email\": \"daniel.freitas@insa.gov.br\", \"matricula\": \"3519383\"}', '{\"login\": \"dfreitas\", \"nome\": \"Daniel de Souza Freitas\", \"dt_nascimento\": \"1989-04-13\", \"dt_admissao\": \"2026-02-02\", \"dt_demissao\": null, \"matricula\": \"3519383\", \"cpf\": \"08052407486\", \"id_situacao\": 1, \"id_carreira\": 1, \"escolaridade\": \"Especialização\", \"titulacao\": null, \"id_responsavel\": 2, \"cep\": \"58416440\", \"logradouro\": \"Av. Floriano Peixoto\", \"complemento\": \"bloco c apto 001\", \"bairro\": \"Santa Rosa\", \"cidade\": \"Campina Grande\", \"estado\": \"PB\", \"telefone\": \"81985454499\", \"email\": \"daniel.freitas@insa.gov.br\", \"genero\": \"M\", \"nivel_acesso\": 1}', '127.0.0.1', '2026-10-21 20:09:19'),
(6, 2, 'pessoa', '2', 'edicao', '{\"nome\": \"Administrador SIGTEC\", \"login\": \"admin.sigtec\", \"email\": \"admin.sigtec@example.invalid\", \"matricula\": \"ADMIN-SIGTEC\"}', '{\"login\": \"admin.sigtec\", \"nome\": \"Administrador SIGTEC\", \"dt_nascimento\": \"2001-10-12\", \"dt_admissao\": \"2026-10-20\", \"dt_demissao\": null, \"matricula\": \"ADMIN-SIGTEC\", \"cpf\": \"000.000.000-01\", \"id_situacao\": 1, \"id_carreira\": null, \"escolaridade\": null, \"titulacao\": null, \"id_responsavel\": null, \"cep\": null, \"logradouro\": null, \"complemento\": null, \"bairro\": null, \"cidade\": null, \"estado\": null, \"telefone\": null, \"email\": \"admin.sigtec@example.invalid\", \"genero\": \"f\", \"nivel_acesso\": 1}', '127.0.0.1', '2026-10-21 20:10:03'),
(8, 3, 'pessoa', '3', 'edicao', '{\"nome\": \"Daniel de Souza Freitas\", \"login\": \"dfreitas\", \"email\": \"daniel.freitas@insa.gov.br\", \"matricula\": \"3519383\"}', '{\"login\": \"dfreitas\", \"nome\": \"Daniel de Souza Freitas\", \"dt_nascimento\": null, \"dt_admissao\": null, \"dt_demissao\": null, \"matricula\": \"3519383\", \"cpf\": \"08052407486\", \"id_situacao\": 1, \"id_carreira\": 1, \"escolaridade\": \"Especialização\", \"titulacao\": null, \"id_responsavel\": 2, \"cep\": \"58416440\", \"logradouro\": \"Av. Floriano Peixoto\", \"complemento\": \"bloco c apto 001\", \"bairro\": \"Santa Rosa\", \"cidade\": \"Campina Grande\", \"estado\": \"PB\", \"telefone\": \"81985454499\", \"email\": \"daniel.freitas@insa.gov.br\", \"genero\": \"M\", \"nivel_acesso\": 1}', '127.0.0.1', '2026-10-21 20:33:01'),
(9, 3, 'pessoa', '1', 'edicao', '{\"nome\": \"Usuario de Teste SIGTEC\", \"login\": \"teste.sigtec\", \"email\": \"teste.sigtec@example.invalid\", \"matricula\": \"TESTE-SIGTEC\"}', '{\"login\": \"teste.sigtec\", \"nome\": \"Usuario de Teste SIGTEC\", \"dt_nascimento\": null, \"dt_admissao\": null, \"dt_demissao\": null, \"matricula\": \"TESTE-SIGTEC\", \"cpf\": \"000.000.000-00\", \"id_situacao\": 1, \"id_carreira\": null, \"escolaridade\": null, \"titulacao\": null, \"id_responsavel\": null, \"cep\": null, \"logradouro\": null, \"complemento\": null, \"bairro\": null, \"cidade\": null, \"estado\": null, \"telefone\": null, \"email\": \"teste.sigtec@example.invalid\", \"genero\": null, \"nivel_acesso\": 3}', '127.0.0.1', '2026-10-21 20:33:33');

-- --------------------------------------------------------

--
-- Estrutura para tabela `nivel_acesso`
--

CREATE TABLE `nivel_acesso` (
  `id` tinyint(4) NOT NULL,
  `descricao` varchar(100) NOT NULL,
  `deletado` tinyint(1) NOT NULL DEFAULT 0
) ;

--
-- Despejando dados para a tabela `nivel_acesso`
--

INSERT INTO `nivel_acesso` (`id`, `descricao`, `deletado`) VALUES
(1, 'Administrador', 0),
(2, 'Gestor', 0),
(3, 'Servidor', 0),
(4, 'Consulta', 0);

-- --------------------------------------------------------

--
-- Estrutura para tabela `pessoa`
--

CREATE TABLE `pessoa` (
  `id` int(11) NOT NULL,
  `login` varchar(100) NOT NULL,
  `senha` varchar(100) NOT NULL COMMENT 'Somente HASH (bcrypt/argon2). Nunca texto puro.',
  `nome` varchar(100) NOT NULL,
  `dt_nascimento` date DEFAULT NULL,
  `dt_admissao` date DEFAULT NULL,
  `dt_demissao` date DEFAULT NULL,
  `matricula` varchar(50) DEFAULT NULL,
  `cpf` varchar(15) NOT NULL,
  `id_situacao` int(11) NOT NULL,
  `id_carreira` int(11) DEFAULT NULL,
  `escolaridade` varchar(100) DEFAULT NULL,
  `titulacao` varchar(100) DEFAULT NULL,
  `id_responsavel` int(11) DEFAULT NULL COMMENT 'Chefia imediata (auto-relacionamento)',
  `cep` varchar(10) DEFAULT NULL,
  `logradouro` varchar(100) DEFAULT NULL,
  `numero` varchar(7) DEFAULT NULL,
  `complemento` varchar(100) DEFAULT NULL,
  `bairro` varchar(100) DEFAULT NULL,
  `cidade` varchar(100) DEFAULT NULL,
  `estado` varchar(3) DEFAULT NULL,
  `telefone` varchar(15) DEFAULT NULL,
  `ramal` varchar(10) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `genero` char(1) DEFAULT NULL COMMENT 'M = Masculino, F = Feminino, O = Outro',
  `nivel_acesso` tinyint(4) NOT NULL DEFAULT 3,
  `deletado` tinyint(1) NOT NULL DEFAULT 0,
  `dt_criacao` timestamp NOT NULL DEFAULT current_timestamp(),
  `dt_atualizacao` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ;

--
-- Despejando dados para a tabela `pessoa`
--

INSERT INTO `pessoa` (`id`, `login`, `senha`, `nome`, `dt_nascimento`, `dt_admissao`, `dt_demissao`, `matricula`, `cpf`, `id_situacao`, `id_carreira`, `escolaridade`, `titulacao`, `id_responsavel`, `cep`, `logradouro`, `numero`, `complemento`, `bairro`, `cidade`, `estado`, `telefone`, `ramal`, `email`, `genero`, `nivel_acesso`, `deletado`, `dt_criacao`, `dt_atualizacao`) VALUES
(1, 'teste.sigtec', 'pbkdf2_sha256$1500000$okHyVTwztqkYLoOaAe4NEc$XxS6E0V25alque0KprqZ2p1eaFadmAWbWg+oj98nfgc=', 'Usuario de Teste SIGTEC', NULL, NULL, NULL, 'TESTE-SIGTEC', '000.000.000-00', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'teste.sigtec@example.invalid', NULL, 3, 0, '2026-10-20 20:45:47', '2026-10-21 20:33:33'),
(2, 'admin.sigtec', 'pbkdf2_sha256$1500000$U9wBB67fdNZkHx1Jleu6zs$+x4eT7h851/PU7OZXREeRLkpkySxddlH86cvo1Ipr0k=', 'Administrador SIGTEC', '2001-10-12', '2026-10-20', NULL, 'ADMIN-SIGTEC', '000.000.000-01', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'admin.sigtec@example.invalid', 'f', 1, 0, '2026-10-21 19:57:51', '2026-10-21 17:29:42'),
(3, 'dfreitas', 'pbkdf2_sha256$1500000$VINEpL4kaSx1Naj4jAGtMg$AJJLSXy+tXnfa1apzerdVXtfX9FTerVn9EusxMhi/oA=', 'Daniel de Souza Freitas', NULL, NULL, NULL, '3519383', '08052407486', 1, 1, 'Especialização', NULL, 2, '58416440', 'Av. Floriano Peixoto', NULL, 'bloco c apto 001', 'Santa Rosa', 'Campina Grande', 'PB', '81985454499', NULL, 'daniel.freitas@insa.gov.br', 'M', 1, 0, '2026-10-21 20:04:15', '2026-10-21 20:33:01');

--
-- Acionadores `pessoa`
--
DELIMITER $$
CREATE TRIGGER `trg_pessoa_responsavel_bu` BEFORE UPDATE ON `pessoa` FOR EACH ROW BEGIN
    IF NEW.id_responsavel IS NOT NULL AND NEW.id_responsavel = NEW.id THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Uma pessoa não pode ser responsável por si mesma.';
    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_pessoa_situacao_ai` AFTER INSERT ON `pessoa` FOR EACH ROW BEGIN
    INSERT INTO pessoa_situacao_historico (id_pessoa, id_situacao_anterior, id_situacao_nova)
    VALUES (NEW.id, NULL, NEW.id_situacao);
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_pessoa_situacao_au` AFTER UPDATE ON `pessoa` FOR EACH ROW BEGIN
    IF NEW.id_situacao <> OLD.id_situacao THEN
        INSERT INTO pessoa_situacao_historico (id_pessoa, id_situacao_anterior, id_situacao_nova)
        VALUES (NEW.id, OLD.id_situacao, NEW.id_situacao);
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estrutura para tabela `pessoa_cargo`
--

CREATE TABLE `pessoa_cargo` (
  `id` int(11) NOT NULL,
  `id_pessoa` int(11) NOT NULL,
  `id_cargo` int(11) NOT NULL,
  `dt_inicio` date NOT NULL,
  `dt_fim` date DEFAULT NULL,
  `atual` tinyint(1) GENERATED ALWAYS AS (if(`dt_fim` is null and `deletado` = 0,1,NULL)) STORED,
  `deletado` tinyint(1) NOT NULL DEFAULT 0
) ;

-- --------------------------------------------------------

--
-- Estrutura para tabela `pessoa_situacao_historico`
--

CREATE TABLE `pessoa_situacao_historico` (
  `id` int(11) NOT NULL,
  `id_pessoa` int(11) NOT NULL,
  `id_situacao_anterior` int(11) DEFAULT NULL,
  `id_situacao_nova` int(11) NOT NULL,
  `dt_alteracao` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Trilha de mudanças de situação funcional';

--
-- Despejando dados para a tabela `pessoa_situacao_historico`
--

INSERT INTO `pessoa_situacao_historico` (`id`, `id_pessoa`, `id_situacao_anterior`, `id_situacao_nova`, `dt_alteracao`) VALUES
(1, 1, NULL, 1, '2026-10-20 17:45:47'),
(2, 2, NULL, 1, '2026-10-21 16:57:51'),
(3, 3, NULL, 1, '2026-10-21 17:04:15');

-- --------------------------------------------------------

--
-- Estrutura para tabela `pessoa_unidade`
--

CREATE TABLE `pessoa_unidade` (
  `id` int(11) NOT NULL,
  `id_pessoa` int(11) NOT NULL,
  `id_unidade` int(11) NOT NULL,
  `dt_inicio` date NOT NULL,
  `dt_fim` date DEFAULT NULL,
  `chefia` tinyint(1) NOT NULL DEFAULT 0 COMMENT '1 = chefe/titular da unidade no período',
  `atual` tinyint(1) GENERATED ALWAYS AS (if(`dt_fim` is null and `deletado` = 0,1,NULL)) STORED,
  `deletado` tinyint(1) NOT NULL DEFAULT 0
) ;

-- --------------------------------------------------------

--
-- Estrutura para tabela `situacao`
--

CREATE TABLE `situacao` (
  `id` int(11) NOT NULL,
  `descricao` varchar(100) NOT NULL,
  `deletado` tinyint(1) NOT NULL DEFAULT 0
) ;

--
-- Despejando dados para a tabela `situacao`
--

INSERT INTO `situacao` (`id`, `descricao`, `deletado`) VALUES
(1, 'Ativo', 0),
(2, 'Afastado', 0),
(3, 'Cedido', 0),
(4, 'Em licença', 0),
(5, 'Aposentado', 0),
(6, 'Exonerado', 0),
(7, 'Desligado', 0);

-- --------------------------------------------------------

--
-- Estrutura para tabela `unidade`
--

CREATE TABLE `unidade` (
  `id` int(11) NOT NULL,
  `descricao` varchar(100) NOT NULL,
  `sigla` varchar(20) DEFAULT NULL,
  `id_unidade_superior` int(11) DEFAULT NULL,
  `deletado` tinyint(1) NOT NULL DEFAULT 0
) ;

--
-- Acionadores `unidade`
--
DELIMITER $$
CREATE TRIGGER `trg_unidade_superior_bu` BEFORE UPDATE ON `unidade` FOR EACH ROW BEGIN
    IF NEW.id_unidade_superior IS NOT NULL AND NEW.id_unidade_superior = NEW.id THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Uma unidade não pode ser superior de si mesma.';
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estrutura stand-in para view `vw_pessoa_detalhada`
-- (Veja abaixo para a visão atual)
--
CREATE TABLE `vw_pessoa_detalhada` (
`id` int(11)
,`nome` varchar(100)
,`login` varchar(100)
,`matricula` varchar(50)
,`cpf` varchar(15)
,`email` varchar(100)
,`telefone` varchar(15)
,`ramal` varchar(10)
,`situacao` varchar(100)
,`carreira` varchar(100)
,`cargo_atual` varchar(100)
,`nivel_cargo` varchar(100)
,`padrao_cargo` varchar(50)
,`unidade_atual` varchar(100)
,`sigla_unidade` varchar(20)
,`responsavel` varchar(100)
,`perfil_acesso` varchar(100)
,`dt_admissao` date
,`dt_demissao` date
);

-- --------------------------------------------------------

--
-- Estrutura para view `vw_pessoa_detalhada`
--
DROP TABLE IF EXISTS `vw_pessoa_detalhada`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_pessoa_detalhada`  AS SELECT `p`.`id` AS `id`, `p`.`nome` AS `nome`, `p`.`login` AS `login`, `p`.`matricula` AS `matricula`, `p`.`cpf` AS `cpf`, `p`.`email` AS `email`, `p`.`telefone` AS `telefone`, `p`.`ramal` AS `ramal`, `s`.`descricao` AS `situacao`, `ca`.`descricao` AS `carreira`, `c`.`cargo` AS `cargo_atual`, `c`.`nivel` AS `nivel_cargo`, `c`.`padrao` AS `padrao_cargo`, `u`.`descricao` AS `unidade_atual`, `u`.`sigla` AS `sigla_unidade`, `r`.`nome` AS `responsavel`, `na`.`descricao` AS `perfil_acesso`, `p`.`dt_admissao` AS `dt_admissao`, `p`.`dt_demissao` AS `dt_demissao` FROM ((((((((`pessoa` `p` join `situacao` `s` on(`s`.`id` = `p`.`id_situacao`)) left join `carreira` `ca` on(`ca`.`id` = `p`.`id_carreira`)) left join `pessoa_cargo` `pc` on(`pc`.`id_pessoa` = `p`.`id` and `pc`.`atual` = 1)) left join `cargo` `c` on(`c`.`id` = `pc`.`id_cargo`)) left join `pessoa_unidade` `pu` on(`pu`.`id_pessoa` = `p`.`id` and `pu`.`atual` = 1)) left join `unidade` `u` on(`u`.`id` = `pu`.`id_unidade`)) left join `pessoa` `r` on(`r`.`id` = `p`.`id_responsavel`)) join `nivel_acesso` `na` on(`na`.`id` = `p`.`nivel_acesso`)) WHERE `p`.`deletado` = 0 ;

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `arquivo`
--
ALTER TABLE `arquivo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `arquivo_id_pessoa_3c508618_fk_pessoa_id` (`id_pessoa`);

--
-- Índices de tabela `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Índices de tabela `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Índices de tabela `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Índices de tabela `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Índices de tabela `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Índices de tabela `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Índices de tabela `cargo`
--
ALTER TABLE `cargo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_cargo_siape` (`siape`);

--
-- Índices de tabela `carreira`
--
ALTER TABLE `carreira`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_carreira_descricao` (`descricao`);

--
-- Índices de tabela `dado_estatistico`
--
ALTER TABLE `dado_estatistico`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dado_estatistico_id_pessoa_282dd9e6_fk_pessoa_id` (`id_pessoa`);

--
-- Índices de tabela `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Índices de tabela `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Índices de tabela `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Índices de tabela `evento`
--
ALTER TABLE `evento`
  ADD PRIMARY KEY (`id`),
  ADD KEY `evento_id_pessoa_8485e7b7_fk_pessoa_id` (`id_pessoa`);

--
-- Índices de tabela `log_auditoria`
--
ALTER TABLE `log_auditoria`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_log_pessoa` (`id_pessoa`),
  ADD KEY `ix_log_tabela_reg` (`tabela`,`id_registro`),
  ADD KEY `ix_log_dt` (`dt_evento`);

--
-- Índices de tabela `nivel_acesso`
--
ALTER TABLE `nivel_acesso`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_nivel_acesso_descricao` (`descricao`);

--
-- Índices de tabela `pessoa`
--
ALTER TABLE `pessoa`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_pessoa_login` (`login`),
  ADD UNIQUE KEY `uq_pessoa_cpf` (`cpf`),
  ADD UNIQUE KEY `uq_pessoa_matricula` (`matricula`),
  ADD KEY `fk_pessoa_nivel_acesso` (`nivel_acesso`),
  ADD KEY `ix_pessoa_nome` (`nome`),
  ADD KEY `ix_pessoa_situacao` (`id_situacao`),
  ADD KEY `ix_pessoa_carreira` (`id_carreira`),
  ADD KEY `ix_pessoa_responsavel` (`id_responsavel`),
  ADD KEY `ix_pessoa_email` (`email`);

--
-- Índices de tabela `pessoa_cargo`
--
ALTER TABLE `pessoa_cargo`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_pc_atual` (`id_pessoa`,`atual`),
  ADD KEY `ix_pc_cargo` (`id_cargo`);

--
-- Índices de tabela `pessoa_situacao_historico`
--
ALTER TABLE `pessoa_situacao_historico`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_psh_ant` (`id_situacao_anterior`),
  ADD KEY `fk_psh_nova` (`id_situacao_nova`),
  ADD KEY `ix_psh_pessoa` (`id_pessoa`,`dt_alteracao`);

--
-- Índices de tabela `pessoa_unidade`
--
ALTER TABLE `pessoa_unidade`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_pu_atual` (`id_pessoa`,`atual`),
  ADD KEY `ix_pu_unidade` (`id_unidade`);

--
-- Índices de tabela `situacao`
--
ALTER TABLE `situacao`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_situacao_descricao` (`descricao`);

--
-- Índices de tabela `unidade`
--
ALTER TABLE `unidade`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_unidade_descricao` (`descricao`),
  ADD KEY `fk_unidade_superior` (`id_unidade_superior`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `arquivo`
--
ALTER TABLE `arquivo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=77;

--
-- AUTO_INCREMENT de tabela `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `cargo`
--
ALTER TABLE `cargo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `carreira`
--
ALTER TABLE `carreira`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `dado_estatistico`
--
ALTER TABLE `dado_estatistico`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de tabela `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de tabela `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de tabela `evento`
--
ALTER TABLE `evento`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `log_auditoria`
--
ALTER TABLE `log_auditoria`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de tabela `pessoa`
--
ALTER TABLE `pessoa`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `pessoa_cargo`
--
ALTER TABLE `pessoa_cargo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `pessoa_situacao_historico`
--
ALTER TABLE `pessoa_situacao_historico`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de tabela `pessoa_unidade`
--
ALTER TABLE `pessoa_unidade`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `situacao`
--
ALTER TABLE `situacao`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `unidade`
--
ALTER TABLE `unidade`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `arquivo`
--
ALTER TABLE `arquivo`
  ADD CONSTRAINT `arquivo_id_pessoa_3c508618_fk_pessoa_id` FOREIGN KEY (`id_pessoa`) REFERENCES `pessoa` (`id`);

--
-- Restrições para tabelas `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Restrições para tabelas `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Restrições para tabelas `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Restrições para tabelas `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Restrições para tabelas `dado_estatistico`
--
ALTER TABLE `dado_estatistico`
  ADD CONSTRAINT `dado_estatistico_id_pessoa_282dd9e6_fk_pessoa_id` FOREIGN KEY (`id_pessoa`) REFERENCES `pessoa` (`id`);

--
-- Restrições para tabelas `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Restrições para tabelas `evento`
--
ALTER TABLE `evento`
  ADD CONSTRAINT `evento_id_pessoa_8485e7b7_fk_pessoa_id` FOREIGN KEY (`id_pessoa`) REFERENCES `pessoa` (`id`);

--
-- Restrições para tabelas `log_auditoria`
--
ALTER TABLE `log_auditoria`
  ADD CONSTRAINT `fk_log_pessoa` FOREIGN KEY (`id_pessoa`) REFERENCES `pessoa` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Restrições para tabelas `pessoa`
--
ALTER TABLE `pessoa`
  ADD CONSTRAINT `fk_pessoa_carreira` FOREIGN KEY (`id_carreira`) REFERENCES `carreira` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_pessoa_nivel_acesso` FOREIGN KEY (`nivel_acesso`) REFERENCES `nivel_acesso` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_pessoa_responsavel` FOREIGN KEY (`id_responsavel`) REFERENCES `pessoa` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_pessoa_situacao` FOREIGN KEY (`id_situacao`) REFERENCES `situacao` (`id`) ON UPDATE CASCADE;

--
-- Restrições para tabelas `pessoa_cargo`
--
ALTER TABLE `pessoa_cargo`
  ADD CONSTRAINT `fk_pc_cargo` FOREIGN KEY (`id_cargo`) REFERENCES `cargo` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_pc_pessoa` FOREIGN KEY (`id_pessoa`) REFERENCES `pessoa` (`id`) ON UPDATE CASCADE;

--
-- Restrições para tabelas `pessoa_situacao_historico`
--
ALTER TABLE `pessoa_situacao_historico`
  ADD CONSTRAINT `fk_psh_ant` FOREIGN KEY (`id_situacao_anterior`) REFERENCES `situacao` (`id`),
  ADD CONSTRAINT `fk_psh_nova` FOREIGN KEY (`id_situacao_nova`) REFERENCES `situacao` (`id`),
  ADD CONSTRAINT `fk_psh_pessoa` FOREIGN KEY (`id_pessoa`) REFERENCES `pessoa` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Restrições para tabelas `pessoa_unidade`
--
ALTER TABLE `pessoa_unidade`
  ADD CONSTRAINT `fk_pu_pessoa` FOREIGN KEY (`id_pessoa`) REFERENCES `pessoa` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_pu_unidade` FOREIGN KEY (`id_unidade`) REFERENCES `unidade` (`id`) ON UPDATE CASCADE;

--
-- Restrições para tabelas `unidade`
--
ALTER TABLE `unidade`
  ADD CONSTRAINT `fk_unidade_superior` FOREIGN KEY (`id_unidade_superior`) REFERENCES `unidade` (`id`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
