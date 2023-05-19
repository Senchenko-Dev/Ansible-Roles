# Инструкция

## Описание

Назначение | Расположение | Описание | Переменные
----------|----------|----------|----------
Установка сервера приложений WildFly | /wildfly/main.yml | Скрипт устанавливает СП WildFly. Для установки в параметрах запуска необходимо передать ссылку на дистрибутив WildFly.  | См. п. __Пререквизиты__

## Пример плейбука
```yml
---
- hosts: all
  tags:
    - always
  vars:
    wf_user: "fly"
    wfadminpass: "fly"
    wf_os_user: "wildfly"
    wf_os_user_pwd: "wildfly"
    wf_os_group: "wfgroup"
    wf_install_dir: "/usr/WF/WF_PPRB"
    executed_by_terraform: "True"
    wildfly_url: "https://github.com/wildfly/wildfly/releases/download/25.0.0.Final/wildfly-25.0.0.Final.zip"  

  tasks:
    - include_role:
        name: wildfly
 ```

## Используемые переменные
Имя переменной | Назначение
----------|----------
wf_service | имя сервиса
wf_install_dir | путь к ВФ
timeout_start_console_wf | ожидание запуска сервиса ВФ
wf_os_user | имя пользователя ВФ (ssh)
wf_os_user_pwd | пароль пользователя ВФ (ssh)
wf_os_group | имя группы ВФ (ssh)
service_name | имя юнита (надо сделать wf_service без .service)
service_dir| путь к env и sh файлам сервиса ("{{ wf_install_dir }}/service")
service_systemd_dir | временная папка "({{ service_dir }}/systemd")
systemd_dir | путь к юнит файлам
nexusUser | пользователь Nexus
nexusPass | пароль пользвателя Nexus
Oracle_jdbc_URL | ссылка на драйвер Oracle (опционально)
PostgreSQL_jdbc_URL | ссылка на драйвер Postgres (опционально) 
wf_user | пользователь ВФ
wfadminpass | пароль пользвателя ВФ
wfapp_service | wildfly.service для wildfly-core.service (надо параметризировать с service_name и wf_service)
 | 
 | 
 |

## На что обратить внимание при устаноке (пререквизиты?)
При использовании скрипта нужно учитывать некоторые особенности:
* В инвентори должны присутствовать переменные:
  * ansible_user
  * ansible_password
* В /tmp должно быть свободное место для распаковки дистрибутива WF.
