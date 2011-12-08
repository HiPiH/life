-- phpMyAdmin SQL Dump
-- version 2.11.4
-- http://www.phpmyadmin.net
--
-- Хост: localhost
-- Время создания: Фев 03 2009 г., 17:33
-- Версия сервера: 5.0.51
-- Версия PHP: 5.2.4-2ubuntu5.4

-- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- Дамп данных таблицы `staticpages_page`
--
INSERT INTO `staticpages_page` (`id`, `title`, `address`, `content`, `published`, `seo_title`, `seo_keywords`, `seo_description`) VALUES
(1, 'О проекте', 'about', 'текст', 1, 'title', 'keywords', 'description'),
(2, 'Текстовая страница', 'tekstovaya-stranica', 'текстовая страница', 1, 'текстовая страница', 'текстовая страница', 'текстовая страница');
