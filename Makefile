#!/usr/bin/make

# You can modify the build mode by passing `BUILD_MODE=DESIRED-BUILD-MODE`
# as a command line argument.
BUILD_MODE			:=	dev

# Checks if the `BUILD_MODE` is a correct one.
ifeq ($(BUILD_MODE),dev)
COMPOSE_FILE		:=	docker-compose.dev.yml
else ifeq ($(BUILD_MODE),prod)
COMPOSE_FILE		:=	docker-compose.prod.yml
else
$(error "$(BUILD_MODE)" is not a valid build mode.)
endif

COMPOSE				:=	docker-compose										\
						--project-name aalms-tr0nscendence-$(BUILD_MODE)	\
						-f $(COMPOSE_FILE)

# Checks for the user executing the Makefile:
# - If they needs root privilege
# - If so, if they have root privilege.
ifneq ($(shell whoami),root)
	ifneq ($(shell docker ps 2>&1 >/dev/null | grep 'permission denied'),)
		ifeq ($(shell sudo -n true 2>&1),)
COMPOSE				:=	sudo $(COMPOSE)
		else
$(error You must acquire root privileges)
		endif
	endif
endif

ifdef NO_PRETTY
COMPOSE				:=	DOCKER_BUILDKIT=0 $(COMPOSE)
endif

all: run

# If the docker is already launched, don't rebuilt it.
# If you want to rebuilt it, use the `build` rule.
ifeq ($(shell $(COMPOSE) ps --services),)
run: build
else
run:
endif
	@$(COMPOSE) up -d

build:
	@$(COMPOSE) build

build-nocache:
	@$(COMPOSE) build --no-cache

down:
	@$(COMPOSE) down

down-volumes:
	@$(COMPOSE) down -v

re: down run

rebuild:		\
		down	\
		build	\
		run

rebuild-nocache:		\
		down-volumes	\
		build-nocache	\
		run

.PHONY:				\
	all				\
	run				\
	build			\
	build-nocache	\
	down			\
	down-volumes	\
	re				\
	rebuild			\
	rebuild-nocache
