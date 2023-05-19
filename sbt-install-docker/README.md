# Ansible Role: Docker

An Ansible Role that installs [Docker](https://www.docker.com) on Linux.

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

    # Edition can be one of: 'ce' (Community Edition) or 'ee' (Enterprise Edition).
    docker_edition: 'ce'
    docker_package: "docker-{{ docker_edition }}"
    docker_package_state: present

The `docker_edition` should be either `ce` (Community Edition) or `ee` (Enterprise Edition). You can also specify a specific version of Docker to install using the distribution-specific format: Red Hat/CentOS: `docker-{{ docker_edition }}-<VERSION>`; Debian/Ubuntu: `docker-{{ docker_edition }}=<VERSION>`.

You can control whether the package is installed, uninstalled, or at the latest version by setting `docker_package_state` to `present`, `absent`, or `latest`, respectively. Note that the Docker daemon will be automatically restarted if the Docker package is updated. This is a side effect of flushing all handlers (running any of the handlers that have been notified by this and any other role up to this point in the play).

    docker_service_state: started
    docker_service_enabled: true
    docker_restart_handler_state: restarted

Variables to control the state of the `docker` service, and whether it should start on boot. If you're installing Docker inside a Docker container without systemd or sysvinit, you should set these to `stopped` and set the enabled variable to `no`.

    docker_install_compose: true
    docker_compose_version: "1.26.0"
    docker_compose_path: /usr/local/bin/docker-compose

Docker Compose installation options.

    docker_apt_release_channel: stable
    docker_apt_arch: amd64
    docker_apt_repository: "deb [arch={{ docker_apt_arch }}] https://download.docker.com/linux/{{ ansible_distribution | lower }} {{ ansible_distribution_release }} {{ docker_apt_release_channel }}"
    docker_apt_ignore_key_error: True
    docker_apt_gpg_key: https://download.docker.com/linux/{{ ansible_distribution | lower }}/gpg

(Used only for Debian/Ubuntu.) You can switch the channel to `nightly` if you want to use the Nightly release.

You can change `docker_apt_gpg_key` to a different url if you are behind a firewall or provide a trustworthy mirror.
Usually in combination with changing `docker_apt_repository` as well.

    docker_yum_repo_url: https://download.docker.com/linux/centos/docker-{{ docker_edition }}.repo
    docker_yum_repo_enable_nightly: '0'
    docker_yum_repo_enable_test: '0'
    docker_yum_gpg_key: https://download.docker.com/linux/centos/gpg

(Used only for RedHat/CentOS.) You can enable the Nightly or Test repo by setting the respective vars to `1`.

You can change `docker_yum_gpg_key` to a different url if you are behind a firewall or provide a trustworthy mirror.
Usually in combination with changing `docker_yum_repository` as well.

    docker_users:
      - user1
      - user2

A list of system users to be added to the `docker` group (so they can use Docker on the server).

    docker_daemon_options:
      storage-driver: "devicemapper"
      log-opts:
        max-size: "100m"

Custom `dockerd` options can be configured through this dictionary representing the json file `/etc/docker/daemon.json`.

## Use with Ansible (and `docker` Python library)

Many users of this role wish to also use Ansible to then _build_ Docker images and manage Docker containers on the server where Docker is installed. In this case, you can easily add in the `docker` role:

## Example Playbook

## Install and Install-deps
```yaml
- hosts: "{{ hosts_group_WF }}"
  max_fail_percentage: 0
  tasks:
  - name: install-deps
    include_role:
      name: docker-install
      tasks_from: install-deps

  - name: install
    include_role:
      name: docker-install
      tasks_from: install
```

## Control
```yaml
- hosts: "{{ hosts_group_WF }}"
  max_fail_percentage: 0
  tasks:
  - name: install
    include_role:
      name: docker-install
      tasks_from: control
    vars:
      docker_control_state: started
```
docs https://docs.ansible.com/ansible/2.9/modules/service_module.html#service-module

Example states

state:
  Choices:
   reloaded
   restarted
   started
   stopped

## Uninstall
```yaml
- hosts: "{{ hosts_group_WF }}"
  max_fail_percentage: 0
  tasks:
  - name: uninstall
    include_role:
      name: docker-install
      tasks_from: uninstall
```

## License

MIT / BSD
