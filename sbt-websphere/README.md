# Ansible Role: WebSphere

An Ansible Role that installs [WebSphere](https://www.ibm.com/ru-ru/cloud/websphere-application-server) on Linux.

## Requirements

None

## Скрипт установки WebSphere

`Шаг 1 - установить заивисимости (подключить repo WebSphere) `</h2><br>
#Для этого нужно запустить playbook <b>install-deps.yaml</b>
который установит заивисимости<br><br>


`Шаг 2 - Запуск установки WebSphere`<br>
#Запускаем playbook <b>install.yaml</b><br><br>


`Чтобы удалить WebSphere`<br>
#Нужно запустить playbook <b>uninstall.yaml</b><br><br>


# Example Playbook

<b>Install-deps</b>
```
---
- hosts: "{{ hosts_group_WF }}"
  become: yes
  tasks:

  - name: inslude_tasks
    include_role:
       name: websphere
       tasks_from: install-deps
```


<b>Install</b>
```
---
- hosts: "{{ hosts_group_WF }}"
  become: yes
  tasks:

  - name: inslude_tasks
    include_role:
       name: websphere
       tasks_from: install
```



<b>Uninstall</b>
```
---
- hosts: "{{ hosts_group_WF }}"
  become: yes
  tasks:

  - name: inslude_tasks
    include_role:
       name: websphere
       tasks_from: uninstall

```
