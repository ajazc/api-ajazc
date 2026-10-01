"""Inicialización del proyecto config.

Activa PyMySQL como driver MySQL compatible con Django
(sin necesidad de compilar mysqlclient en Windows).
"""
import pymysql

pymysql.install_as_MySQLdb()