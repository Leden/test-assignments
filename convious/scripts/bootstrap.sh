#!/bin/sh

set -e

C_RED="\033[31m"
C_GREEN="\033[32m"
C_BOLD="\033[1m"
C_DEFAULT="\033[0m"

OK="${C_GREEN}${C_BOLD}OK${C_DEFAULT}"
FAIL="${C_RED}${C_BOLD}FAIL${C_DEFAULT}"

ORIGIN_URL='https://github.com/vilantis/cookiecutter-django'

die() {
	case "$1" in
		[0-9]) code="$1" ; msg="$2" ;;
		*) code=1 ; msg="$1" ;;
	esac

	printf '%b\n' "$msg"
	exit "$code"
}

verlte() {
	[ "$1" = "$(printf '%s\n%s' "$1" "$2" | sort -V | head -n1)" ]
}

verify_version() {
	name="$1"
	shift
	required_version="$1"
	shift
	cmd="$1"
	get_version_cmd="$*"

	printf 'Checking %b version... ' "$name"
	command -v "$cmd" >/dev/null || die "$name not found. $FAIL"
	version="$($get_version_cmd | head -n1)"
	printf '%b: ' "${C_BOLD}$version${C_DEFAULT}"
	verlte "$required_version" "$version" || \
		die "Required version is ${C_BOLD}$required_version${C_DEFAULT}. $FAIL"
	printf '%b\n' "$OK"
}

verify_git_repo() {
	printf 'Checking git repo... '
	git rev-parse 2>/dev/null || die "Not a git repo. Use ${C_BOLD}git init${C_DEFAULT} first. $FAIL"
	printf '%b\n' "$OK"
}

install_poetry() {
	printf 'Checking poetry... '
	(command -v poetry >/dev/null && poetry --version) || {
		printf 'Not found. Installing... '
		python -m pip install poetry
		command -v asdf && asdf reshim
	}
	printf '%b\n' "$OK"
}

install_precommit() {
	cd backend
	poetry install
	venv_path="$(poetry env info -p)"
	. "$venv_path/bin/activate"
	cd ..
	pre-commit install
}

commit() {
	git add .
	git commit -m "Bootstrapped from ${ORIGIN_URL}"
}

print_start_instructions() {
	printf 'Initial setup is complete. You can now launch vote for places to lunch today with %b command.\n' \
		"${C_BOLD}make start${C_DEFAULT}"
	printf 'To reset the database to its initial state, use %b.\n' "${C_BOLD}make reset-db${C_DEFAULT}"
	printf 'See the %b for more useful commands.\n' "${C_BOLD}Makefile${C_DEFAULT}"
}

main() {
	verify_version "Docker" "18.06.1" docker version -f '{{.Server.Version}}'
	verify_version "Docker Compose" "1.24.1" docker-compose version --short
	verify_version "Python" "Python 3.11" python --version
	verify_version "GNU Make" "GNU Make 4.1" make --version

	verify_git_repo

	install_poetry
	install_precommit

	commit
	make build

	print_start_instructions
}

main
