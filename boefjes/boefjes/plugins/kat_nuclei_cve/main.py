import subprocess


def run(boefje_meta: dict) -> list[tuple[set, bytes | str]]:
    url = boefje_meta["arguments"]["input"]["name"]
    cmd = ["/usr/local/bin/nuclei"] + boefje_meta["arguments"]["oci_arguments"] + ["-u", url]

    output = subprocess.run(cmd, capture_output=True)
    output.check_returncode()

    return [({"openkat/nuclei-cve-output"}, output.stdout.decode())]
