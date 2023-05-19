#!/bin/bash
export VAULT_PASS="123456"
time ansible-playbook playbook_prereq.yml -i inventory -l local:nginx_iag_ii --vault-password-file ./vault.sh