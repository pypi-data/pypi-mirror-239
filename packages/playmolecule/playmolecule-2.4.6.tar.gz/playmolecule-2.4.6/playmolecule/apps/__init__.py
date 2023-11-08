# (c) 2015-2023 Acellera Ltd http://www.acellera.com
# All Rights Reserved
# Distributed under HTMD Software License Agreement
# No redistribution in whole or part
#
from glob import glob
import os
from jinja2 import Environment, PackageLoader, select_autoescape
from playmolecule._appfiles import _File, _Artifacts, _get_app_files
from playmolecule._tests import _Tests
import shutil

# Do not remove unused imports. They are used in the jinja file probably
from pathlib import Path
import os
import stat
import logging
import enum


logger = logging.getLogger(__name__)


_app_list = []


env = Environment(
    loader=PackageLoader("playmolecule", "share"),
    autoescape=select_autoescape(["*"]),
)


@enum.unique
class JobStatus(enum.IntEnum):
    """Job status codes describing the current status of a job

    * WAITING_INFO : Waiting for status from the job. Job has not started yet computation.
    * RUNNING : Job is currently running
    * COMPLETED : Job has successfully completed
    * ERROR : Job has exited with an error
    """

    WAITING_INFO = 0
    RUNNING = 1
    COMPLETED = 2
    ERROR = 3

    def describe(self):
        codes = {0: "Waiting info", 1: "Running", 2: "Completed", 3: "Error"}
        return codes[self.value]

    def __str__(self):
        return self.describe()


JOB_TIMEOUT = 60  # Timeout after which if there is no newer date in .pm.alive we consider the job dead


class ExecutableDirectory:
    """Executable directory class.

    All app functions will create a folder and return to you an `ExecutableDirectory` object.
    This is a self-contained directory including all app input files which can be executed either locally or on a cluster.
    If it's not executed locally make sure the directory can be accessed from all machines
    in the cluster (i.e. is located on a shared filesystem).
    """

    def __init__(self, dirname, _execution_resources=None) -> None:
        self.dirname = dirname
        self.execution_resources = _execution_resources

    @property
    def status(self):
        """Returns current status of the ExecutableDirectory

        Examples
        --------
        >>> ed = proteinprepare(outdir="test", pdbid="3ptb")
        >>> ed.slurm(ncpu=1, ngpu=0)
        >>> print(ed.status)
        """
        import datetime
        import json

        if os.path.exists(os.path.join(self.dirname, ".pm.done")):
            return JobStatus.COMPLETED
        elif os.path.exists(os.path.join(self.dirname, ".pm.err")):
            return JobStatus.ERROR

        heartbeat = os.path.join(self.dirname, ".pm.alive")
        if os.path.exists(heartbeat):
            with open(heartbeat, "r") as f:
                timestamp_str = f.read().strip()
                timestamp = None

                if len(timestamp_str):
                    try:
                        timestamp = datetime.datetime.fromisoformat(timestamp_str)
                    except Exception:
                        logger.error(f"Malformed timestamp in {heartbeat}")

                if timestamp is not None:
                    diff = datetime.datetime.now() - timestamp
                    if diff > datetime.timedelta(seconds=JOB_TIMEOUT):
                        return JobStatus.ERROR
                    else:
                        return JobStatus.RUNNING

        # Alternatively check if expected outputs exist
        outputs = os.path.join(self.dirname, "expected_outputs.json")
        if os.path.exists(outputs):
            with open(outputs, "r") as f:
                outputs = json.load(f)

            for outf in outputs:
                if not os.path.exists(outf):
                    return JobStatus.RUNNING
            else:
                return JobStatus.COMPLETED

        raise RuntimeError(
            f"Could not determine job status for directory {self.dirname}. Talk with the app devs to see what they messed up."
        )

    def run(self, queue=None, **kwargs):
        """Execute the directory locally

        If no queue is specified it will run the job locally.

        Examples
        --------
        >>> ed = proteinprepare(outdir="test", pdbid="3ptb")
        >>> ed.run()

        Specifying a queue

        >>> ed.run(queue="slurm", partition="normalCPU", ncpu=3, ngpu=1)

        Alternative syntax for

        >>> ed.slurm(partition="normalCPU", ncpu=3, ngpu=1)
        """
        if queue is None:
            import subprocess

            subprocess.call(["bash", "run.sh"], cwd=self.dirname)
        else:
            if queue.lower() == "slurm":
                self.slurm(**kwargs)

    def slurm(self, **kwargs):
        """Submit simulations to SLURM cluster

        Parameters
        ----------
        partition : str or list of str
            The queue (partition) or list of queues to run on. If list, the one offering earliest initiation will be used.
        jobname : str
            Job name (identifier)
        priority : str
            Job priority
        ncpu : int
            Number of CPUs to use for a single job
        ngpu : int
            Number of GPUs to use for a single job
        memory : int
            Amount of memory per job (MiB)
        gpumemory : int
            Only run on GPUs with at least this much memory. Needs special setup of SLURM. Check how to define gpu_mem on
            SLURM.
        walltime : int
            Job timeout (s)
        mailtype : str
            When to send emails. Separate options with commas like 'END,FAIL'.
        mailuser : str
            User email address.
        outputstream : str
            Output stream.
        errorstream : str
            Error stream.
        nodelist : list
            A list of nodes on which to run every job at the *same time*! Careful! The jobs will be duplicated!
        exclude : list
            A list of nodes on which *not* to run the jobs. Use this to select nodes on which to allow the jobs to run on.
        envvars : str
            Envvars to propagate from submission node to the running node (comma-separated)
        prerun : list
            Shell commands to execute on the running node before the job (e.g. loading modules)

        Examples
        --------
        >>> ed = proteinprepare(outdir="test", pdbid="3ptb")
        >>> ed.slurm(partition="normalCPU", ncpu=3, ngpu=1)
        """
        from jobqueues.slurmqueue import SlurmQueue

        sl = SlurmQueue()

        if self.execution_resources is not None:
            # Set app defaults
            for arg in self.execution_resources:
                setattr(sl, arg, self.execution_resources[arg])

        # Set user-specified arguments
        for arg in kwargs:
            setattr(sl, arg, kwargs[arg])

        sl.submit(self.dirname)
        return sl


_validators = {
    "str": str,
    "Path": (str, Path, _File),
    "bool": bool,
    "int": (int, float),
    "float": (int, float),
    "dict": dict,
}


def _write_inputs(write_dir, arguments, manifest):
    import json

    inputdir = os.path.join(write_dir, "inputs")
    os.makedirs(inputdir, exist_ok=True)

    if "outputs" in manifest:
        with open(os.path.join(write_dir, "expected_outputs.json"), "w") as f:
            json.dump(manifest["outputs"], f)

    # Validate arg types and copy Path arguments to folder
    for arg in manifest["params"]:
        name = arg["name"]
        argtype = arg["type"]
        nargs = None if "nargs" not in arg else arg["nargs"]

        vals = arguments[name]
        if nargs is None and isinstance(vals, (list, tuple)):
            raise RuntimeError(
                f"Argument '{name}' was passed value '{vals}' which is of type '{type(vals).__name__}'. Was expecting a single value of type '{argtype}'."
            )
        if not isinstance(vals, (list, tuple)):
            vals = [vals]

        # Validate type
        if argtype in _validators:
            validator = _validators[argtype]
            for val in vals:
                if val is not None and not isinstance(val, validator):
                    raise RuntimeError(
                        f"Argument '{name}' was passed value '{val}' which is of type '{type(val).__name__}'. Was expecting value of type '{argtype}'."
                    )
        else:
            logger.warning(
                f"Could not find validator for type: {arg['type']}. Please notify the PM developers."
            )

        # Copy Path-type arguments to folder
        if (
            argtype == "Path"
            and name in arguments
            and name not in ("outdir", "scratchdir")
        ):
            newvals = []
            for val in vals:
                if val is None:
                    continue

                if isinstance(val, _File):
                    newvals.append(val.path)
                    continue  # Don't copy artifacts

                val = os.path.abspath(val)

                outname = os.path.join(inputdir, os.path.basename(val))
                i = 0
                while os.path.exists(outname):
                    parts = os.path.splitext(os.path.basename(val))
                    outname = os.path.join(inputdir, f"{parts[0]}_{i}{parts[1]}")
                    i += 1

                if os.path.isdir(val):
                    shutil.copytree(val, outname)
                else:
                    shutil.copy(val, outname)
                newvals.append(os.path.relpath(outname, write_dir))

            if len(newvals) == 0:
                arguments[name] = None
            elif len(newvals) == 1:
                arguments[name] = newvals[0]
            else:
                arguments[name] = newvals

    with open(os.path.join(inputdir, "inputs.json"), "w") as f:
        json.dump(arguments, f, indent=4)


def _docs_from_manifest(manifest, appname):
    from copy import deepcopy

    manifest = deepcopy(manifest)

    if "description" not in manifest:
        raise RuntimeError(
            "Missing the 'description' field in your app manifest with a description of the app."
        )

    docs = [manifest["description"], "", "Parameters", "----------"]
    for i, param in enumerate(manifest["params"]):
        pp = f"{param['name']} : {param['type']}"
        if "choices" in param and param["choices"] is not None:
            choices = '", "'.join(param["choices"])
            pp += f', choices=("{choices}")'
        docs.append(pp)
        docs.append(f"    {param['description']}")

    missing = []

    if "outputs" in manifest:
        docs.append("")
        docs.append("Outputs")
        docs.append("-------")
        for key, val in manifest["outputs"].items():
            docs.append(key)
            docs.append(f"    {val}")
    else:
        missing.append("outputs")

    if "examples" in manifest:
        docs.append("")
        docs.append("Examples")
        docs.append("--------")
        for exp in manifest["examples"]:
            docs.append(f">>> {exp}")
    else:
        missing.append("examples")

    if "tests" in manifest:
        for test_name in manifest["tests"]:
            desc = manifest["tests"][test_name]["description"]
            args = manifest["tests"][test_name]["arguments"]
            args_str = ""
            for key, vals in args.items():
                if not isinstance(vals, (list, tuple)):
                    vals = [vals]
                for i in range(len(vals)):
                    val = vals[i]
                    if isinstance(val, str):
                        if val.startswith("tests/"):
                            val = f"{appname}.files['{val}']"
                        elif val.startswith("datasets/"):
                            logger.info(
                                "Deprecate datasets in favour of artifacts or files"
                            )
                            val = val.replace("datasets/", "")
                            val = f"{appname}.datasets.{val}"
                        elif val.startswith("artifacts/"):
                            val = val.replace("artifacts/", "")
                            val = f"{appname}.artifacts.{val}"
                        else:
                            val = f"'{val}'"
                    vals[i] = val
                if len(vals) > 1:
                    args_str += f"{key}=[{', '.join(map(str, vals))}], "
                else:
                    args_str += f"{key}={vals[0]}, "

            docs.append("")
            docs.append(desc)
            docs.append(f">>> {appname}(outdir='./out', {args_str[:-2]}).run()")

        if "examples" in missing:  # if there are tests don't complain about examples
            missing.remove("examples")

    if "name" not in manifest:
        missing.append("name")
    else:
        appname = manifest["name"]

    if len(missing):
        logger.warning(f"{appname} manifest is missing fields: {', '.join(missing)}")
    return docs


def _args_from_manifest(manifest):
    # Fix for old apps
    fix_old_types = {"string": "str", "file": "Path"}

    # Arguments which don't have a "value" field should be mandatory
    for arg in manifest["params"]:
        if "mandatory" not in arg:
            arg["mandatory"] = "value" not in arg

    args = []
    # Ensure mandaroty args come first if someone messes up the manifest
    mand_params = [x for x in manifest["params"] if x["mandatory"]]
    opt_params = [x for x in manifest["params"] if not x["mandatory"]]

    params = mand_params + opt_params
    for i, param in enumerate(params):
        atype = param["type"]
        if atype in fix_old_types:
            atype = fix_old_types[atype]
        if atype == "str_to_bool":
            atype = "bool"

        atype_final = atype
        if "nargs" in param and param["nargs"] is not None:
            atype_final = f"list[{atype}]"

        argstr = f"{param['name']} : {atype_final}"

        if not param["mandatory"]:
            default = param["value"]
            if atype in ("str", "Path") and param["value"] is not None:
                default = f"\"{param['value']}\""

            # Fix for old apps
            if atype not in ("str", "Path") and param["value"] == "":
                default = None

            argstr += f" = {default}"

        if i != len(params) - 1:
            argstr += ","
        args.append(argstr)
    return args


def _manifest_to_func(appname, app_versions, latest):
    app_info = {}
    for version in app_versions:
        manifest = app_versions[version]["manifest"]
        try:
            app_info[version] = {
                "args": _args_from_manifest(manifest),
                "docs": _docs_from_manifest(manifest, appname),
                "run.sh": app_versions[version]["run.sh"],
                "manifest": app_versions[version]["manifest"],
                "appdir": app_versions[version]["appdir"],
            }
        except Exception:
            import traceback

            logger.error(
                f"Failed to parse manifest for app {manifest['name']} version {version} with error: {traceback.format_exc()}"
            )

    if len(app_info) == 0:
        return

    template = env.get_template("func.py.jinja")
    fstring = template.render(
        app_info=app_info,
        app_name=appname,
        class_name=appname.capitalize(),
        latest=latest,
    )
    exec(fstring)


def _set_root(root_dir):
    import json
    from natsort import natsorted
    import playmolecule

    if root_dir.startswith("http"):
        from playmolecule._pmws import _set_root_pmws

        _set_root_pmws(root_dir)
        return

    logger.info(f"PlayMolecule home: {root_dir}")

    _setup_folders(root_dir)

    for app_d in natsorted(glob(os.path.join(root_dir, "apps", "*", ""))):
        appname = os.path.basename(os.path.abspath(app_d))
        versions = glob(os.path.join(app_d, "*"))
        versions.sort(key=lambda s: natsorted(os.path.basename(s)))

        app_versions = {}
        for vv in versions:
            vname = os.path.basename(vv)

            jf = glob(os.path.join(vv, "*.json"))
            if len(jf) > 1:
                print(f"ERROR: Multiple json files found in {vv}")
            if len(jf) == 1 and os.stat(jf[0]).st_size != 0:
                try:
                    with open(jf[0]) as f:
                        app_versions[vname] = {
                            "manifest": json.load(f),
                            "appdir": vv,
                            "run.sh": os.path.join(vv, "run.sh"),
                        }
                except Exception as e:
                    logger.error(
                        f"Failed at parsing manifest JSON file {jf[0]} with error: {e}"
                    )
        if len(app_versions):
            _manifest_to_func(appname, app_versions, vname)

    dsdir = os.path.join(root_dir, "datasets")
    dsjson = os.path.join(dsdir, "datasets.json")
    if os.path.exists(dsdir) and os.path.exists(dsjson):
        with open(dsjson) as f:
            manifest = json.load(f)
        playmolecule.datasets = _Artifacts(manifest, dsdir)


def _setup_folders(root_dir):
    os.makedirs(root_dir, exist_ok=True)
    os.makedirs(os.path.join(root_dir, "apps"), exist_ok=True)
    os.makedirs(os.path.join(root_dir, "datasets"), exist_ok=True)

    apptainer_runner = os.path.join(root_dir, "apptainer_run.sh")
    if not os.path.exists(apptainer_runner):
        try:
            import questionary

            license_type = questionary.select(
                "Do you use a floating license server (IP/Port) or a license file?:",
                choices=["Floating License Server", "License File"],
                default="Floating License Server",
                use_shortcuts=True,
            ).unsafe_ask()
            if license_type == "Floating License Server":
                license_ip = questionary.text(
                    message="Type the IP/URL of the license server:"
                ).unsafe_ask()
                license_port = questionary.text(
                    message="Type the port of the license server:", default="27000"
                ).unsafe_ask()
                license_file = f"{license_port}@{license_ip}"
            else:
                license_file = questionary.path(
                    message="Path to license file:",
                ).unsafe_ask()
                new_lic_file = os.path.join(root_dir, "license.dat")
                shutil.copy(license_file, new_lic_file)
                license_file = new_lic_file
        except KeyboardInterrupt:
            raise RuntimeError("PlayMolecule setup cancelled...")

        template = env.get_template("apptainer_run.sh")
        fstring = template.render(
            license_file_or_server=license_file,
            root_dir=root_dir,
        )
        with open(apptainer_runner, "w") as f:
            f.write(fstring)

        st = os.stat(apptainer_runner)
        os.chmod(
            apptainer_runner, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        )

        with open(os.path.join(root_dir, "license_path.txt"), "w") as f:
            f.write(license_file)

    if len(glob(os.path.join(root_dir, "apps", "*", ""))) == 0:
        from playmolecule._update import update_apps

        update_apps()
