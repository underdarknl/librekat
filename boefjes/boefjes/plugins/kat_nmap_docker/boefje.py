import base64
import logging
import subprocess
import sys
from enum import Enum
from ipaddress import IPv6Address, ip_address
from typing import List, Optional

import requests

PROTOCOL_DEFAULT = "tcp"
TOP_PORTS_MAX = 65535
TOP_PORTS_DEFAULT = 250
TOP_PORTS_MIN = 1

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kat_nmap_docker")


class Protocol(Enum):
    TCP = "tcp"
    UDP = "udp"


def build_nmap_arguments(host: str, protocol: Protocol, top_ports: Optional[int]) -> List[str]:
    """Returns Nmap arguments to use based on protocol and top_ports for host."""
    ip = ip_address(host)
    args = [
        "--open",
        "-T4",
        "-Pn",
        "-r",
        "-v10",
        "-sV",
        "-sS" if protocol == Protocol.TCP else "-sU",
    ]
    if top_ports is None:
        args.append("-p-")
    else:
        args.extend(["--top-ports", str(top_ports)])

    if isinstance(ip, IPv6Address):
        args.append("-6")

    args.extend(["-oX", "-", host])

    return args


if __name__ == "__main__":
    input_url = sys.argv[1]
    logger.info("task input url: %s", input_url)

    resp = requests.get(input_url)
    resp.raise_for_status()
    task_input = resp.json()
    logger.debug("task input: %s", task_input)
    boefje_meta = task_input["boefje_meta"]

    if "TOP_PORTS" in boefje_meta["environment"]:
        top_ports = int(boefje_meta["environment"]["TOP_PORTS"])
    else:
        top_ports = TOP_PORTS_DEFAULT
    logger.debug("top_ports: %d", top_ports)
    assert (
        TOP_PORTS_MIN <= top_ports <= TOP_PORTS_MAX
    ), f'{TOP_PORTS_MIN} <= {top_ports} <= {TOP_PORTS_MAX} fails. Check "TOP_PORTS" argument.'

    if "PROTOCOL" in boefje_meta["environment"]:
        protocol = boefje_meta["environment"]["PROTOCOL"].lower()
    else:
        protocol = PROTOCOL_DEFAULT
    logger.debug("protocol: %s", protocol)

    assert protocol in ["tcp", "udp"], f'Invalid protocol "{protocol}".'

    args = [
        "/usr/bin/nmap",
        *build_nmap_arguments(boefje_meta["arguments"]["input"]["address"], Protocol(protocol), top_ports),
    ]
    logger.info("Nmap args: %s", args)

    try:
        nmap = subprocess.run(args, capture_output=True, check=True)
    except subprocess.CalledProcessError as e:
        logger.exception("Nmap subprocess error")
        logger.error("Nmap subprocess stdout: %s", e.stdout.decode())
        logger.error("Nmap subprocess stderr: %s", e.stderr.decode())
        raise

    output_url = task_input["output_url"]
    file = {
        "name": "nmap.xml",
        "content": base64.b64encode(nmap.stdout).decode("utf-8"),
        "tags": ["nmap", "application/xml"],
    }
    resp = requests.post(output_url, json={"status": "COMPLETED", "files": [file]})
    resp.raise_for_status()
