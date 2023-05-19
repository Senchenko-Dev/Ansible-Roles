# Скрипты автоматизации настройки серверов NGINX (IAG)

Скрипты предназначены для автоматичекой настройки серверов перед использованием Автоматичекской установки дистрибутива nginx-iag.

## Конфигурация

Для серверов, на которых будет производиться настройка ОС необходимо:
- Заполнить inventory
- Заполнить vars.yml
- Заполнить _passwords.conf

### Mitogen
Для ускорения выполнения роли используется mitogen. В случае появления ошибки при выполнении таска "get password parameters from _passwords.conf" mitogen следует отключить в файле ansible .cfg

### Заполнение vars.yml
```yaml
  prereq_nginx_iag_privileged_user: "ansible-deploy-user" # Priveleged with sudo user
  # LVMs
  # В переменных задаются значения для создания LV
  prereq_nginx_iag_mounts: /# Определение переменной для создания LVM
    nginx-iag:
      size: 256 # Размер создаваемого LV. При указании размера в мегабайтах пишем число. При указании размера в гигабайтах указывается 5g
      mount_name: "tcpdump" # Имя mount
      vg_name: "rootvg" # Имя volume group
      lv_name: "tcpdump" # Имя создаваемого LV
      mount_path: "/var/tcpdump" # Точка монтирования
      dev_path: "/dev/mapper/rootvg-tcpdump" # Путь к блочному устройству
      owner: "nginx-iag" # Владелец
      group: "nginx-iag" # Группа
      filesystem: ext4 # Тип файловой системы
    opt:
      size: "100%FREE" # Размер создаваемого LV
      mount_name: "opt"
      vg_name: "rootvg"
      lv_name: "rootvg-lvopt"
      mount_path: "/opt"
      dev_path: "/dev/mapper/rootvg-lvopt"
      owner: "root"
      group: "root"
      filesystem: ext4

  # Mounts and limits
  # В переменных задаются лимиты для проверки размера разделов
  prereq_nginx_iag_limits:
    root:
      mountpoint: "/"
      disk_free_limit: "50" # Размер задается в гигабайтах
    nginx-iag:
      mountpoint: "/opt"
      disk_free_limit: "0.1"
  /#  tcpdump:
  /#    mountpoint: "/var/tcpdump"
  /#    disk_free_limit: "0.1"

  # Users and groups
  # В переменных задаются пользователи и группы, в которые пользователь будет добавлен
  prereq_nginx_iag_user_group:
    nginx-iag:
      username: "nginx-iag"
      usergroup: "nginx-iag"
      homedir: "/home/nginx-iag"
      groups: "nginx-iag, efs_tester"
      expires: -1
    log_rsys:
      username: "log_rsys"
      usergroup: "log_rsys"
      homedir: "/home/log_rsys"
      groups: "nginx-iag, log_rsys, efs_tester"
      expires: -1
    efs_tester:
      username: "efs_tester"
      usergroup: "efs_tester"
      homedir: "/home/efs_tester"
      groups: "nginx-iag, log_rsys"
      expires: -1

  # Settings for iac_admin_efs user
  # В переменных задаются пользователь, его uid и группы, в которые пользователь будет добавлен
  prereq_nginx_iag_iac_admin_efs:
    iac_admin_efs:
      username: "iac_admin_efs"
      usergroup: "iac_admin_efs"
      homedir: "/home/iac_admin_efs"
      shell: "/bin/bash"
      uid: 11998
      expires: -1

  # Sysctl values
  # В переменных задаются значения для добавления sysctl
  prereq_nginx_iag_sysctl_config: # Sysctl dict vars
    net.core.netdev_max_backlog: 10000
    net.core.somaxconn: 9600
    net.ipv4.tcp_syncookies: 1
    net.ipv4.tcp_max_syn_backlog: 9600
    net.ipv4.tcp_max_tw_buckets: 720000
    net.ipv4.tcp_tw_recycle: 1
    net.ipv4.tcp_timestamps: 1
    net.ipv4.tcp_tw_reuse: 1
    net.ipv4.tcp_fin_timeout: 30
    net.ipv4.tcp_keepalive_time: 1800
    net.ipv4.tcp_keepalive_probes: 7
    net.ipv4.tcp_keepalive_intvl: 30
    net.core.wmem_max: 33554432
    net.core.rmem_max: 33554432
    net.core.rmem_default: 8388608
    net.core.wmem_default: 4194394
    net.ipv4.tcp_rmem: 4096 8388608 16777216
    net.ipv4.tcp_wmem: 4096 4194394 16777216

  # libs url
  # В переменной prereq_nginx_iag_rsysloglib_url задается url, откуда будет скачан дистрибутив
 # SIGMA: https://nexus.swec.sbercloud.ru/nexus/content/repositories/Nexus_PROD/Nexus_PROD/CI00360902_TECH_CORE/D-09.004.03-01/CI00360902_TECH_CORE-D-09.004.03-01-distrib.zip
 # ALFA: http://mirror.ca.sbrf.ru/packages/generic/rsyslog-iag/rsyslog_libraries-1.0.tar.gz

  prereq_nginx_iag_rsysloglib_url: "http://mirror.sigma.sbrf.ru/packages/generic/rsyslog_iag/rsyslog_libraries-1.0.tar.gz"
  # /etc/rc.local values
  # В переменной задаюется имя сетевого интерфейса для добавления в /etc/rc.local
  prereq_nginx_iag_rc_local:
    interface_name: "eth0"
```

### Пароль для расшифровки _passwords.conf
Пароль для расшифровки _passwords.conf должен храниться в переменной окружения VAULT_PASS

### Настройка _passwords.conf
Для расшифровки _passwords.conf необходимо использовать комманду:
*openssl aes-256-cbc -d -in _passwords.conf -out _passwords.conf.plain*
Для зашифровки _passwords.conf необходимо использовать комманду:
*openssl enc -aes-256-cbc -in _passwords.conf.plain -out _passwords.conf*
Расшифрованный файл _passwords.conf.plain необходимо редактировать в vim

В файле _passwords.conf указываются пароли для создаваемых пользователей в формате:
*prereq_nginx_iag.<username defined in vars.yml>.password="<password>"*

## Использование

Пример запуска плейбука: run.sh