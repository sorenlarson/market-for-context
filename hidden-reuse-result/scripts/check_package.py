#!/usr/bin/env python3
"""Cold-start checks for the publication package."""

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "AGENTS.md",
    "README.md",
    "FULL-EXPOSITION.md",
    "INTERROGATE.md",
    "MODEL.md",
    "RESULT.md",
    "FIRM-SIZE-RESULT.md",
    "FIRM-SIZE-DRAFT.md",
    "OWNERSHIP-ACCESS-RESULT.md",
    "OWNERSHIP-ACCESS-DRAFT.md",
    "APPROPRIATION-RESULT.md",
    "APPROPRIATION-DRAFT.md",
    "REFERENCES.md",
    "WEBSITE-DRAFT.md",
    "PUBLISHING.md",
    "FIGURE.md",
    "LICENSE.md",
    "CITATION.cff",
    "pyproject.toml",
    "requirements-lock.txt",
    "Makefile",
    "src/hidden_reuse/model.py",
    "src/hidden_reuse/pledgeability.py",
    "src/hidden_reuse/firm_size.py",
    "src/hidden_reuse/ownership_access.py",
    "src/hidden_reuse/appropriation.py",
    "tests/test_model.py",
    "tests/test_firm_size.py",
    "tests/test_ownership_access.py",
    "tests/test_appropriation.py",
    "scripts/generate_figures.py",
    "scripts/generate_pledgeability.py",
    "scripts/generate_examples.py",
    "scripts/solve_scenario.py",
    "scripts/solve_pricing.py",
    "scripts/solve_private_signal.py",
    "scripts/generate_firm_size.py",
    "scripts/solve_firm_size.py",
    "scripts/generate_ownership_access.py",
    "scripts/solve_ownership_access.py",
    "scripts/generate_appropriation.py",
    "scripts/solve_appropriation.py",
    "outputs/hidden-reuse-regime-map.png",
    "outputs/hidden-reuse-regime-map.svg",
    "outputs/hidden-reuse-regime-grid.csv",
    "outputs/hidden-reuse-run-summary.json",
    "outputs/worked-examples.json",
    "outputs/hidden-reuse-explorer.html",
    "outputs/capability-pledgeability-map.png",
    "outputs/capability-pledgeability-map.svg",
    "outputs/capability-pledgeability-grid.csv",
    "outputs/pledgeability-run-summary.json",
    "outputs/pledgeability-examples.json",
    "outputs/firm-size-separation-map.png",
    "outputs/firm-size-separation-map.svg",
    "outputs/firm-size-entry-grid.csv",
    "outputs/firm-size-scale-grid.csv",
    "outputs/firm-size-run-summary.json",
    "outputs/firm-size-examples.json",
    "outputs/ownership-access-regime-map.png",
    "outputs/ownership-access-regime-map.svg",
    "outputs/ownership-access-topology.png",
    "outputs/ownership-access-topology.svg",
    "outputs/ownership-access-grid.csv",
    "outputs/ownership-access-robustness.csv",
    "outputs/ownership-access-run-summary.json",
    "outputs/ownership-access-examples.json",
    "outputs/ownership-access-explorer.html",
    "outputs/value-appropriation-regime-map.png",
    "outputs/value-appropriation-regime-map.svg",
    "outputs/value-appropriation-grid.csv",
    "outputs/pareto-capture-benchmark.csv",
    "outputs/value-appropriation-robustness.csv",
    "outputs/value-appropriation-run-summary.json",
    "outputs/value-appropriation-examples.json",
    "outputs/value-appropriation-explorer.html",
]

MARKDOWN_FILES = [
    "README.md",
    "FULL-EXPOSITION.md",
    "INTERROGATE.md",
    "MODEL.md",
    "RESULT.md",
    "FIRM-SIZE-RESULT.md",
    "FIRM-SIZE-DRAFT.md",
    "OWNERSHIP-ACCESS-RESULT.md",
    "OWNERSHIP-ACCESS-DRAFT.md",
    "APPROPRIATION-RESULT.md",
    "APPROPRIATION-DRAFT.md",
    "REFERENCES.md",
    "WEBSITE-DRAFT.md",
    "PUBLISHING.md",
    "FIGURE.md",
]


def local_link_errors(path: Path):
    errors = []
    text = path.read_text(encoding="utf-8")
    for raw_target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
        target = raw_target.strip().split("#", 1)[0]
        if not target or "://" in target or target.startswith(("mailto:", "#")):
            continue
        decoded = target.replace("%20", " ")
        if not (path.parent / decoded).resolve().exists():
            errors.append(f"{path.relative_to(ROOT)} -> {raw_target}")
    return errors


def main() -> None:
    missing = [relative for relative in REQUIRED if not (ROOT / relative).exists()]
    broken = []
    for relative in MARKDOWN_FILES:
        path = ROOT / relative
        if path.exists():
            broken.extend(local_link_errors(path))

    metadata_errors = []
    if not missing:
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
        package_init = (ROOT / "src/hidden_reuse/__init__.py").read_text(
            encoding="utf-8"
        )
        summary = json.loads(
            (ROOT / "outputs/hidden-reuse-run-summary.json").read_text(encoding="utf-8")
        )
        pledgeability_summary = json.loads(
            (ROOT / "outputs/pledgeability-run-summary.json").read_text(
                encoding="utf-8"
            )
        )
        firm_size_summary = json.loads(
            (ROOT / "outputs/firm-size-run-summary.json").read_text(encoding="utf-8")
        )
        ownership_access_summary = json.loads(
            (ROOT / "outputs/ownership-access-run-summary.json").read_text(
                encoding="utf-8"
            )
        )
        appropriation_summary = json.loads(
            (ROOT / "outputs/value-appropriation-run-summary.json").read_text(
                encoding="utf-8"
            )
        )
        version_patterns = {
            "pyproject.toml": re.search(
                r'^version = "([^"]+)"$', pyproject, flags=re.MULTILINE
            ),
            "CITATION.cff": re.search(
                r"^version: ([^\s]+)$", citation, flags=re.MULTILINE
            ),
            "src/hidden_reuse/__init__.py": re.search(
                r'^__version__ = "([^"]+)"$', package_init, flags=re.MULTILINE
            ),
        }
        versions = {
            name: match.group(1) if match else None
            for name, match in version_patterns.items()
        }
        versions["run summary"] = summary.get("model_version")
        versions["pledgeability run summary"] = pledgeability_summary.get(
            "model_version"
        )
        versions["firm-size run summary"] = firm_size_summary.get("model_version")
        versions["ownership-access run summary"] = ownership_access_summary.get(
            "model_version"
        )
        versions["value-appropriation run summary"] = appropriation_summary.get(
            "model_version"
        )
        if len(set(versions.values())) != 1 or None in versions.values():
            metadata_errors.append(f"version mismatch: {versions}")

        status = summary.get("result_status", "")
        if "not empirical evidence" not in status:
            metadata_errors.append("run summary is missing the claim-status warning")
        pledgeability_status = pledgeability_summary.get("result_status", "")
        if "not empirical evidence" not in pledgeability_status:
            metadata_errors.append(
                "pledgeability summary is missing the claim-status warning"
            )
        firm_size_status = firm_size_summary.get("result_status", "")
        if "not empirical evidence" not in firm_size_status:
            metadata_errors.append(
                "firm-size summary is missing the claim-status warning"
            )
        ownership_access_status = ownership_access_summary.get("result_status", "")
        if "not empirical evidence" not in ownership_access_status:
            metadata_errors.append(
                "ownership-access summary is missing the claim-status warning"
            )
        appropriation_status = appropriation_summary.get("result_status", "")
        if "not empirical evidence" not in appropriation_status:
            metadata_errors.append(
                "value-appropriation summary is missing the claim-status warning"
            )

        with (ROOT / "outputs/hidden-reuse-regime-grid.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            header = set(next(csv.reader(handle)))
        required_columns = {
            "regime",
            "agreement",
            "disclosure",
            "monitoring",
            "reuse",
            "provider_reuse_gain_before_enforcement",
            "required_monitoring_to_deter",
            "payment_cap_binding",
        }
        if not required_columns.issubset(header):
            metadata_errors.append(
                f"CSV missing columns: {sorted(required_columns - header)}"
            )

        with (ROOT / "outputs/capability-pledgeability-grid.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            pledgeability_header = set(next(csv.reader(handle)))
        pledgeability_columns = {
            "verifiable_share",
            "collateral",
            "expected_net_capability_value",
            "maximum_pledgeable_payment",
            "pledgeable_share",
            "unpledgeable_expected_value",
            "regime",
        }
        if not pledgeability_columns.issubset(pledgeability_header):
            metadata_errors.append(
                "Pledgeability CSV missing columns: "
                f"{sorted(pledgeability_columns - pledgeability_header)}"
            )

        with (ROOT / "outputs/firm-size-entry-grid.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            firm_entry_header = set(next(csv.reader(handle)))
        firm_entry_columns = {
            "internalization_advantage",
            "cross_node_learning",
            "integration_threshold",
            "conditional_target_size",
            "equilibrium_firm_size",
            "per_node_surplus_at_target",
            "regime",
        }
        if not firm_entry_columns.issubset(firm_entry_header):
            metadata_errors.append(
                "Firm-entry CSV missing columns: "
                f"{sorted(firm_entry_columns - firm_entry_header)}"
            )

        with (ROOT / "outputs/firm-size-scale-grid.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            firm_scale_header = set(next(csv.reader(handle)))
        firm_scale_columns = {
            "integration_cost_scale",
            "integration_cost_elasticity",
            "organization_cost_scale",
            "cross_node_learning",
            "integration_threshold",
            "conditional_target_size",
            "continuous_target_size",
        }
        if not firm_scale_columns.issubset(firm_scale_header):
            metadata_errors.append(
                "Firm-scale CSV missing columns: "
                f"{sorted(firm_scale_columns - firm_scale_header)}"
            )

        with (ROOT / "outputs/ownership-access-grid.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            ownership_header = set(next(csv.reader(handle)))
        ownership_columns = {
            "network",
            "external_learning_efficiency",
            "neutrality_penalty",
            "regime",
            "ownership_size",
            "owned_names",
            "incremental_value",
            "selection_margin",
        }
        if not ownership_columns.issubset(ownership_header):
            metadata_errors.append(
                "Ownership-access CSV missing columns: "
                f"{sorted(ownership_columns - ownership_header)}"
            )

        with (ROOT / "outputs/ownership-access-robustness.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            robustness_header = set(next(csv.reader(handle)))
        robustness_columns = {
            "scenario",
            "regime",
            "probability",
            "mean_ownership_size",
            "draws",
            "seed",
        }
        if not robustness_columns.issubset(robustness_header):
            metadata_errors.append(
                "Ownership robustness CSV missing columns: "
                f"{sorted(robustness_columns - robustness_header)}"
            )

        with (ROOT / "outputs/value-appropriation-grid.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            appropriation_header = set(next(csv.reader(handle)))
        appropriation_columns = {
            "external_learning_efficiency",
            "platform_capture_share",
            "equivalent_pareto_tail_index",
            "regime",
            "ownership_size",
            "incremental_private_value",
            "capture_upgrade",
            "productive_learning_upgrade",
            "external_access_slope",
        }
        if not appropriation_columns.issubset(appropriation_header):
            metadata_errors.append(
                "Value-appropriation CSV missing columns: "
                f"{sorted(appropriation_columns - appropriation_header)}"
            )

        with (ROOT / "outputs/pareto-capture-benchmark.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            pareto_header = set(next(csv.reader(handle)))
        pareto_columns = {
            "tail_index",
            "monopoly_price",
            "provider_profit",
            "customer_surplus",
            "provider_capture_share",
            "pricing_deadweight_loss",
        }
        if not pareto_columns.issubset(pareto_header):
            metadata_errors.append(
                "Pareto benchmark CSV missing columns: "
                f"{sorted(pareto_columns - pareto_header)}"
            )

        with (ROOT / "outputs/value-appropriation-robustness.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            appropriation_robustness_header = set(next(csv.reader(handle)))
        appropriation_robustness_columns = {
            "scenario",
            "regime",
            "frequency",
            "mean_ownership_size",
            "draws",
            "seed",
        }
        if not appropriation_robustness_columns.issubset(
            appropriation_robustness_header
        ):
            metadata_errors.append(
                "Value-appropriation robustness CSV missing columns: "
                f"{sorted(appropriation_robustness_columns - appropriation_robustness_header)}"
            )

        svg = (ROOT / "outputs/hidden-reuse-regime-map.svg").read_text(encoding="utf-8")
        if "<title id=" not in svg or "<desc id=" not in svg:
            metadata_errors.append("SVG is missing accessible title or description")
        pledgeability_svg = (
            ROOT / "outputs/capability-pledgeability-map.svg"
        ).read_text(encoding="utf-8")
        if (
            "<title id=" not in pledgeability_svg
            or "<desc id=" not in pledgeability_svg
        ):
            metadata_errors.append(
                "pledgeability SVG is missing accessible title or description"
            )
        firm_size_svg = (ROOT / "outputs/firm-size-separation-map.svg").read_text(
            encoding="utf-8"
        )
        if "<title id=" not in firm_size_svg or "<desc id=" not in firm_size_svg:
            metadata_errors.append(
                "firm-size SVG is missing accessible title or description"
            )
        for label, relative in {
            "ownership-access": "outputs/ownership-access-regime-map.svg",
            "ownership-topology": "outputs/ownership-access-topology.svg",
            "value-appropriation": "outputs/value-appropriation-regime-map.svg",
        }.items():
            source = (ROOT / relative).read_text(encoding="utf-8")
            if "<title id=" not in source or "<desc id=" not in source:
                metadata_errors.append(
                    f"{label} SVG is missing accessible title or description"
                )

    if missing or broken or metadata_errors:
        if missing:
            print("Missing required files:")
            for relative in missing:
                print(f"  - {relative}")
        if broken:
            print("Broken local links:")
            for link in broken:
                print(f"  - {link}")
        if metadata_errors:
            print("Metadata or output errors:")
            for error in metadata_errors:
                print(f"  - {error}")
        raise SystemExit(1)

    print(
        f"Package audit passed: {len(REQUIRED)} required files, "
        f"{len(MARKDOWN_FILES)} Markdown documents, version metadata, "
        "CSV schema, and SVG accessibility checked."
    )


if __name__ == "__main__":
    main()
