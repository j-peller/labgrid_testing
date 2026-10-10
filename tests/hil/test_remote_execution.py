import os
import xml.etree.ElementTree as ET
import pytest

LOCAL_BINARY = "build-target/target_unit_tests"
REMOTE_DIR = "/home/runner/hil_workspace"
REMOTE_BINARY = f"{REMOTE_DIR}/target_unit_tests"
REMOTE_REPORT = f"{REMOTE_DIR}/results.xml"
LOCAL_REPORT_DIR = "reports"

def test_crosscompiled_firmware_on_target(target):
    ssh = target.get_driver("SSHDriver")

    assert os.path.exists(LOCAL_BINARY), f"Missing artifact: {LOCAL_BINARY}"

    # Transfer to target
    ssh.run(f"mkdir -p {REMOTE_DIR}")
    ssh.put(LOCAL_BINARY, REMOTE_BINARY)
    ssh.run(f"chmod +x {REMOTE_BINARY}")

    # Run GoogleTest generating JUnit XML
    cmd = f"{REMOTE_BINARY} --gtest_output=xml:{REMOTE_REPORT}"
    stdout, stderr, exit_code = ssh.run(cmd)

    # Pull XML back to runner
    os.makedirs(LOCAL_REPORT_DIR, exist_ok=True)
    local_report = os.path.join(LOCAL_REPORT_DIR, "target_results.xml")
    try:
        ssh.get(REMOTE_REPORT, local_report)
    finally:
        ssh.run(f"rm -rf {REMOTE_DIR}")

    # Assertions
    assert exit_code == 0, f"Tests failed:\n{''.join(stdout)}\n{''.join(stderr)}"

    tree = ET.parse(local_report)
    root = tree.getroot()
    failures = int(root.attrib.get("failures", 0))
    errors = int(root.attrib.get("errors", 0))
    assert failures == 0 and errors == 0, f"{failures} failures, {errors} errors found."
