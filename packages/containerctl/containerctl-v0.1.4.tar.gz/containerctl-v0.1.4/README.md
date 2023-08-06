containerctl
============
A tool for building and running [Docker][2] containers.

Configuration
-------------
The containerctl commandline utility loads [Docker][2] container information from a `container.yml`
file in the current directory or the provided `path` directory which is an option to each command.
The `container.yml` file determines the user, name, version, path, and [fig][3] configuration of
the container.

The following directives are supported:

* `name` - The name part of the Docker tag. If of the form `user/name` the user part is
  copied into `user`. This is the only required value.
* `user` - The user part of the Docker tag. 
* `version` - Set to hardcode the version part of the container tag.
* `path` - The path to the directory containing the container's Dockerfile and context. Defaults to
  the path value provided to containerctl which is usually cwd.
* `prebuild` - A command to execute just prior to calling `docker build` on a container.
* `running` - [Fig][3] configuration. Used to run the container. The values of `user`, `name`,
  `tag`, and `version` may be substituted into the [fig][3] configuration using the double-brace
  syntax. So, for instance, {{tag}} would be replaced with the full tag name of the container.
* `testing` - Additional [Fig][3] configuration used by the test command. Containers defined here
  are used in addition to those found in `running`. Nameing a container in `testing` the same as
  one in `running` will replace that container. There must be a container named `test` for the test
  command to work. This container is run using `fig run`. The exit code of the command should be
  used to determine the success of the tests.

The following config example would allow you to build an nginx container and run it with an example
website located in a separate container:

    name: example/nginx
    running:
        site:
            image: example/website
        nginx:
            image: {{tag}}
            ports:
            - 80
            volumes_from:
            - site
    testing:
        test:
            build: tests
            links:
            - nginx:www.example.net

Prebuild
--------
containerctl supports executing a script just prior to a build. By convention this should be an
executable file called `prebuild` in the container directory. If this file exists it will be
executed. A different prebuild command may be excuted by setting the `prebuild` configuration
directive.

Version Detection
-----------------
If no version is provided in the config file an attempt is made to detect the version of the
container. First the existance of an executable called `version` is checked for in the container
directory. If found the first line of this executable's output is used.

If the `version` executable does not exist an attempt is made to determine the current git tag of
the repository the container resides in. This will fail if the container is not in a git repo or
the git command is missing. If HEAD is not tagged then the short form of the commit hash is
appended to `rev-` to create a commit specific version.

Should none of the above attempts yield a version the container version will fall back to the
default value of `latest`.

Available Commands
------------------
The following commands are available to containerctl:

* `build` - Build the container. The container is tagged as `user/name:version`.
* `info` - Print information about the container.
* `push` - Push the container to the remote repository.
* `rm` - Remove the container's image from Docker.
* `run` - Run the container. Requires [fig][3].
* `test` - Test the container. Requires [fig][3]. Runs the defined test container.

These are just brief descriptions. See `containerctl help COMMAND` for full usage details of each.

License
-------
Copyright (c) 2014 Wifast, Inc. This project and all of its contents is
licensed under the BSD-derived license as found in the included [LICENSE][1]
file.

[1]: https://github.com/WiFast/containerctl/blob/master/LICENSE "LICENSE"
[2]: https://www.docker.com "Docker"
[3]: http://www.fig.sh/ "Fig"
