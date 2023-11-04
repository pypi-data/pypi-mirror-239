import asyncio
import glob
import os
import sys
from grpc_tools import protoc as grpc_tools_protoc
from importlib import resources
from resemble.cli.directories import (
    chdir,
    dot_rsm_directory,
    is_on_path,
    use_working_directory,
)
from resemble.cli.rc import ArgumentParser, BaseTransformer, TransformerError
from resemble.cli.subprocesses import Subprocesses
from resemble.cli.terminal import fail, info, warn
from resemble.cli.watch import watch
from typing import Optional, Set

RESEMBLE_SPECIFIC_PLUGINS = {
    'python': ['--python_out', '--grpc_python_out', '--resemble_python_out'],
    'react': ['--es_out', '--resemble_react_out'],
}


class GenerateTransformer(BaseTransformer):

    def transform(self, value: str):
        plugins = value.split(',')
        for plugin in plugins:
            if plugin not in RESEMBLE_SPECIFIC_PLUGINS:
                raise TransformerError(
                    f"Invalid flag '--generate={value}': '{plugin}' is not a valid plugin. "
                    f"Resemble supported plugins: {', '.join(RESEMBLE_SPECIFIC_PLUGINS)}"
                )
        return plugins


def register_protoc(parser: ArgumentParser):
    parser.subcommand('protoc').add_argument(
        '--working-directory',
        type=str,
        help="directory in which to execute",
        required=True,
    )

    parser.subcommand('protoc').add_argument(
        '--output-directory',
        type=str,
        help="output directory in which `protoc` will generate files",
        required=True,
    )

    parser.subcommand('protoc').add_argument(
        '--watch',
        type=bool,
        default=False,
        help="watches specified 'protos' for changes and re-runs `protoc`"
    )

    parser.subcommand('protoc').add_argument(
        '--wait-for-changes',
        type=bool,
        default=False,
        help="wait for any changes to '.proto' files before running `protoc'"
    )

    parser.subcommand('protoc').add_argument(
        '--verbose',
        type=bool,
        default=False,
        help="whether or not to be verbose"
    )

    parser.subcommand('protoc').add_argument(
        '--generate',
        type=str,
        help=
        "Resemble specific plugins that will be invoked by `protoc` separated "
        "by comma (','). Uses all Resemble specific plugins by default.",
        transformer=GenerateTransformer(),
        default=','.join(RESEMBLE_SPECIFIC_PLUGINS),
    )

    parser.subcommand('protoc').add_argument(
        'proto_directories',
        type=str,
        help="proto directory(s) which will (1) be included as import paths "
        "and (2) be recursively searched for '.proto' files to compile",
        repeatable=True,
        required=True,
    )


async def ensure_protoc_gen_es(subprocesses: Subprocesses):
    """Helper to ensure we have 'protoc-gen-es' and its dependencies
    installed.

    We install these in the '.rsm' directory, by placing an empty
    'package.json' file and then running 'npm install' as
    necessary. This approach makes it so that we don't have to bundle
    'protoc-gen-es' as part of our pip package.
    """
    if not is_on_path('npm'):
        fail(
            "We require 'npm' and couldn't find it on your PATH. "
            "Is it installed?"
        )

    if not is_on_path('node'):
        fail(
            "We require 'node' and couldn't find it on your PATH. "
            "Is it installed?"
        )

    os.makedirs(dot_rsm_directory(), exist_ok=True)

    with chdir(dot_rsm_directory()):
        if (
            not os.path.isfile('package.json') or
            os.path.getsize('package.json') == 0
        ):
            with open('package.json', 'w') as file:
                file.write('{}')

        # Check and see if we've already installed 'protobuf-gen-es'
        # and if not install it and its dependencies. We redirect
        # stdout/stderr to a pipe and only print it out if any of our
        # commands fail.
        async with subprocesses.shell(
            'npm list @bufbuild/protoc-gen-es',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        ) as process:
            stdout, _ = await process.communicate()

            if process.returncode != 0:
                info("Installing 'es' protoc plugin")

                async with subprocesses.shell(
                    'npm install @bufbuild/protobuf && npm install @bufbuild/protoc-gen-es',
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.STDOUT,
                ) as process:
                    stdout, _ = await process.communicate()

                    if process.returncode != 0:
                        fail(
                            "\n"
                            f"Failed to install 'protobuf-gen-es':\n"
                            f"{stdout.decode() if stdout is not None else '<no output>'}"
                            "\n"
                            "Please report this bug to the maintainers."
                        )


def get_value_of_arg_in_argv(
    arg: str,
    argv: list[str],
) -> Optional[str]:
    """Pulls the value out of `argv_after_dash_dash` for `arg`. Handles both
    args that include an '=' and those that don't, e.g.
    '--resemble_react_out path' or '--resemble_react_out=path'.
    """
    for i in range(len(argv)):
        protoc_arg = argv[i]
        if protoc_arg.startswith(arg):
            if '=' not in protoc_arg:
                if len(argv) - 1 == i:
                    fail(f'Missing value for {arg}, try '
                         f'{arg}=VALUE')
                else:
                    return argv[i + 1]
            else:
                return protoc_arg.split('=', 1)[1]

    return None


async def protoc(
    args,
    argv_after_dash_dash: list[str],
    parser: ArgumentParser,
):
    """Invokes `protoc` with the arguments passed to 'rsm protoc'."""
    # Determine the working directory and move into it.
    with use_working_directory(args.working_directory, parser):

        # Use `Subprocesses` to manage all of our subprocesses for us.
        subprocesses = Subprocesses()

        def user_specified_explicit(arg: str):
            """Helper for checking if the user explicitly specified an argument."""
            return any(
                [
                    protoc_arg.startswith(arg) or arg in protoc_arg
                    for protoc_arg in argv_after_dash_dash
                ]
            )

        def fail_if_plugin_specified_incorrect(plugin, plugin_out_flags):
            """Helper for checking if the user specified the correct plugin.
            We require '--generate=python' to be specified if one of
            '--python_out', '--grpc_python_out', '--resemble_python_out' is
            specified explicitly.
            We require '--generate=react' to be specified if one of
            '--es_out', '--resemble_react_out' is specified explicitly."""
            if plugin not in args.generate:
                for plugin_out_flag in plugin_out_flags:
                    if user_specified_explicit(plugin_out_flag):
                        parser._parser.error(
                            "You've specified an output directory via "
                            f"{plugin_out_flag} but you haven't "
                            f"asked us to generate it via --generate={plugin}"
                        )

        for (plugin, plugin_out_flags) in RESEMBLE_SPECIFIC_PLUGINS.items():
            fail_if_plugin_specified_incorrect(plugin, plugin_out_flags)

        # Fill in `protoc` args based on our args.
        protoc_args: list[str] = ["grpc_tool.protoc"]

        # We want to find the Python `site-packages`/`dist-packages` directories
        # that contain a 'resemble/v1alpha1' directory, which is where we'll
        # find our protos. We can look for the 'resemble' folder via the
        # `resources` module; the resulting path is a `MultiplexedPath`, since
        # there may be multiple. Such a path doesn't contain a `parent`
        # attribute, since there isn't one answer. Instead we use `iterdir()` to
        # get all of the children of all 'resemble' folders, and then
        # deduplicate the parents-of-the-parents-of-those-children (via the
        # `set`), which gives us the `resemble` folders' parents' paths.
        resemble_parent_paths: set[str] = set()
        for path in resources.files('resemble').iterdir():
            resemble_parent_paths.add(str(path.parent.parent))

        if len(resemble_parent_paths) == 0:
            raise FileNotFoundError(
                "Failed to find 'resemble' resource path. "
                "Please report this bug to the maintainers."
            )

        # Now add these to '--proto_path', so that users don't need to provide
        # their own Resemble protos.
        for resemble_parent_path in resemble_parent_paths:
            protoc_args.append(f"--proto_path={resemble_parent_path}")

        # User protos may rely on `google.protobuf.*` protos. We
        # conveniently have those files packaged in our Python
        # package; make them available to users, so that users don't
        # need to provide them.
        protoc_args.append(
            f"--proto_path={resources.files('grpc_tools').joinpath('_proto')}"
        )

        # Now set flags, e.g., '--python_out' '--grpc_python_out',
        # '--resemble_out', etc, to `args.output_directory` if they
        # are not already specified explicitly.
        def user_specified_explicit(arg: str):
            """Helper for checking if the user explicitly specified an argument."""
            return any(
                [
                    protoc_arg.startswith(arg)
                    for protoc_arg in argv_after_dash_dash
                ]
            )

        output_directory = args.output_directory

        plugins_using_output_directory: Set[str] = set()

        python_out_path: Optional[str] = None

        # Now set flags, e.g., '--python_out' '--grpc_python_out',
        # '--resemble_python_out', etc, to `args.output_directory` if they
        # are not already specified explicitly.
        if 'python' in args.generate:
            if not is_on_path('protoc-gen-resemble_python'):
                raise FileNotFoundError(
                    "Failed to find 'protoc-gen-resemble_python'. "
                    "Please report this bug to the maintainers."
                )
            if user_specified_explicit('--python_out'):

                # Determine the value of '--python_out'. It may come in
                # the form '--python_out=VALUE' or '--python_out VALUE'.
                # We will use this path for protoc '--python_out',
                # '--grpc_python_out' and '--resemble_python_out'
                # unless they are set explicitly.
                python_out_path = get_value_of_arg_in_argv(
                    '--python_out', argv_after_dash_dash
                )
                assert python_out_path is not None
            else:
                protoc_args.append(f'--python_out={output_directory}')
                plugins_using_output_directory.add("'python'")

            if not user_specified_explicit('--grpc_python_out'):
                if python_out_path is None:
                    protoc_args.append(f'--grpc_python_out={output_directory}')
                    plugins_using_output_directory.add("'python'")
                else:
                    protoc_args.append(f'--grpc_python_out={python_out_path}')

            if not user_specified_explicit('--resemble_python_out'):
                if python_out_path is None:
                    protoc_args.append(
                        f'--resemble_python_out={output_directory}'
                    )
                    plugins_using_output_directory.add("'python'")
                else:
                    protoc_args.append(
                        f'--resemble_python_out={python_out_path}'
                    )

        # Add 'protoc-gen-es' plugin if 'react' is specified in
        # '--generate' otherwise we do fail earlier.
        if 'react' in args.generate:
            if not is_on_path('protoc-gen-resemble_react'):
                raise FileNotFoundError(
                    "Failed to find 'protoc-gen-resemble_react'. "
                    "Please report this bug to the maintainers."
                )

            await ensure_protoc_gen_es(subprocesses)

            protoc_args.append(
                f"--plugin={os.path.join(dot_rsm_directory(), 'node_modules', '.bin', 'protoc-gen-es')}"
            )

            resemble_react_out_path = None

            if not user_specified_explicit('--resemble_react_out'):
                protoc_args.append(f'--resemble_react_out={output_directory}')
                plugins_using_output_directory.add("'react'")
            else:
                resemble_react_out_path = get_value_of_arg_in_argv(
                    '--resemble_react_out', argv_after_dash_dash
                )
                assert resemble_react_out_path is not None

                # If the user specified a react out path but that path does not
                # exist, create it.
                #
                # This is a _much_ better experience than the error message
                # that `protoc` gives if the directory does not exist.
                if not os.path.isdir(resemble_react_out_path):
                    os.mkdir(resemble_react_out_path)

            if not user_specified_explicit('--es_out'):
                if resemble_react_out_path is not None:
                    protoc_args.append(f'--es_out={resemble_react_out_path}')
                else:
                    protoc_args.append(f'--es_out={output_directory}')
                plugins_using_output_directory.add("'react'")
            else:
                if resemble_react_out_path is None:
                    fail(
                        "Must specify '--resemble_react_out' if you specify '--es_out'"
                    )

                es_out_path = get_value_of_arg_in_argv(
                    '--es_out', argv_after_dash_dash
                )
                assert es_out_path is not None

                if resemble_react_out_path != es_out_path:
                    fail(
                        "'--resemble_react_out' must be the same as '--es_out' "
                        f"(you specified '--resemble_react_out={resemble_react_out_path}' "
                        f"and '--es_out={es_out_path}')"
                    )

                # If the user specified an es out path but that path does not
                # exist, create it.
                #
                # This is a _much_ better experience than the error message
                # that `protoc` gives if the directory does not exist.
                if os.path.isdir(es_out_path):
                    os.mkdir(es_out_path)

        if len(plugins_using_output_directory) == 0:
            warn(
                f"Ignoring --output-directory={args.output_directory} in favor "
                "of the explicitly specified output directories set after --\n"
            )

        # TODO(benh): in the future only generate the following
        # warning if we are not using the output directory for ALL of
        # the files that we are generating.
        if len(plugins_using_output_directory) > 0:
            warn(
                f"Using output directory '{output_directory}' "
                f"for generated {', '.join(plugins_using_output_directory)} files. "
                "Use '--output-directory=DIRECTORY' to override it "
                "(or use the `protoc` args, e.g., '--python_out=DIRECTORY', to "
                "explicitly specify output for particular languages or plugins).\n"
            )
            os.makedirs(output_directory, exist_ok=True)

        # Add all args after '--'.
        protoc_args += argv_after_dash_dash

        # Grab all of the positional '.proto' arguments.
        proto_directories: list[str] = args.proto_directories or []

        protos = []

        for proto_directory in proto_directories:
            # Expand any directories to be short-form for 'directory/**/*.proto'.
            if not os.path.isdir(proto_directory):
                fail(f"Failed to find directory '{proto_directory}'")
            else:
                # Also add any directories given to us as part of the import path.
                protoc_args.append(f'--proto_path={proto_directory}')
                found_protos = False
                for file in glob.iglob(
                    os.path.join(proto_directory, '**', '*.proto'),
                    recursive=True,
                ):
                    _, extension = os.path.splitext(file)
                    if extension == '.proto':
                        found_protos = True
                        protos.append(file)

                if not found_protos:
                    fail(
                        f"'{proto_directory}' did not match any '.proto' files"
                    )

        protoc_args += protos

        # Indicates whether or not we should wait for changes to
        # '.proto' files initially or run immediately. We'll reuse
        # this variable for watching below.
        wait_for_changes = args.wait_for_changes

        while True:
            if wait_for_changes:
                async with watch(protos) as file_system_event_task:
                    await file_system_event_task

            if not args.verbose:
                info(
                    'Running `protoc ...` (use --verbose to see full command)'
                )
            else:
                info('protoc')
                for arg in protoc_args[1:]:
                    info(f'  {arg}')

            returncode = grpc_tools_protoc.main(protoc_args)

            if not args.watch:
                return returncode
            else:
                wait_for_changes = True

                # Print a new line between each invocation.
                print()

                continue
