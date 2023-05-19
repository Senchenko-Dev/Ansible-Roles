# Ansible Role: Kubernetes

An Ansible Role that installs [Kubernetes](https://kubernetes.io/) on Linux.

## Requirements

None

## Скрипт установки Kubernetes

`Шаг 1 - установить заивисимости (подключить repo) Kubernetes`</h2><br>
#Для этого нужно запустить playbook <b>install-deps.yaml</b>
который установит заивисимости<br><br>


`Шаг 2 - Запуск установки кубернетес`<br>
#Запускаем playbook <b>install.yaml</b><br><br>


`Шаг 3 - Установка Dashboard`<br>
#Запускаем playbook <b>install-dashboard.yaml</b><br><br>


`Шаг 4 - Запуск создание namespaces`<br>
#Запусукаем playbook <b>create-namespaces.yaml</b><br><br>


`Чтобы удалить кластер`<br>
#Нужно запустить playbook <b>uninstall.yaml</b><br><br>
	
	
# Example Playbook

<b>Instal-deps</b>
```
---
- hosts: all
  become: yes
  tasks:
  - name: inslude_tasks
    include_role:
       name: sbt-install-kubernetes
       tasks_from: install-deps
```


<b>Install</b>
```
--- 
- hosts: all
  become: yes
  tasks:

  - name: inslude_tasks
    include_role:
       name: sbt-install-kubernetes
       tasks_from: install
```


	   
<b>Instal-dashboard</b>
```
---
- hosts: all
  become: yes
  tasks:

  - name: inslude_tasks
    include_role:
       name: sbt-install-kubernetes
       tasks_from: install-dashboard
```	
    
    
<b>Create-namespaces</b>
```
--- 
- hosts: all
  vars_files:
    - "{{ WORKSPACE }}/config/{{Stand}}/{{Subsystem}}/{{ system_conf_WF | default('system.conf') }}"
  
    
  tasks:
  - name: Temp dir
    tempfile:
      state: directory
      suffix: tokens
    register: tokens
    

  - name: inslude_tasks
    include_role:
       name: sbt-install-kubernetes
       tasks_from: create-namespaces
    vars:
      token_dir: "{{ tokens.path }}"
      custom_namespace_name: "{{ item }}"
    with_items: "{{ namespaces_list }}"
  

  - name: Archive
    archive:
      path: "{{ tokens.path }}/tokens"
      dest: /tmp/mytoken.zip
      format: zip
  
  
  - name: Delete token file on host
    file:
      path: /tmp/mytoken.zip
      state: absent
```

<b>Uninstall</b>
```
---
- hosts: all
  become: yes
  tasks:

  - name: inslude_tasks
    include_role:
       name: sbt-install-kubernetes
       tasks_from: uninstall
```





  	
	
