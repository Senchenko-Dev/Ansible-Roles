# Ansible Role: Nginx

An Ansible Role that installs [Nginx](https://nginx.org/) on Linux.

## Requirements

None


## Скрипт установки Nginx

`Шаг 1 - установить заивисимости Nginx`</h2><br>
#Для этого нужно запустить playbook <b>install-deps.yaml</b>
который установит заивисимости<br><br>


`Шаг 2 - Запуск установки Nginx`<br>
#Запускаем playbook <b>install.yaml</b><br><br>


`Шаг 3 - Запуск mount диска Nginx`<br>
#Запускаем playbook <b>mount-disk.yaml</b><br><br>


`Чтобы удалить Nginx`<br>
#Нужно запустить playbook <b>uninstall-nginx.yaml</b><br><br>


# Example Playbook

<b>Install-deps</b>
```
--- 
- hosts: all
  become: yes
  tasks:
  - name: inslude_tasks
    include_role:
       name: sbt-install-nginx
       tasks_from: install-deps
```

<br/>

<b>Install-nginx</b>
```
--- 
- hosts: all
  become: yes
  tasks:
  - name: inslude_tasks
    include_role:
       name: sbt-install-nginx
       tasks_from: install
```

<br/>

<b>mount-disk</b>
```
---
- hosts: all
  become: yes
  tasks:
    - debug:
        var: disks
    - name: inslude_tasks
      vars:
        mount_point: "{{item.mount_point}}"
        device: "/dev/sd{{array_label_disk[my_index]}}"
      with_items: "{{disks}}"
      loop_control:
        index_var: my_index
      include_role:
        name: sbt-install-nginx
        tasks_from: install-disks
```

<br/>

<b>uninstall-nginx</b>
```
--- 
- hosts: "localhost"
  become: yes
  tasks:
  - name: inslude_tasks
    include_role:
       name: sbt-install-nginx
       tasks_from: uninstall
```