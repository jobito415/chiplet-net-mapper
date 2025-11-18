#!/usr/bin/env python3
import os
import argparse

import pandas as pd
import yaml


def load_c4(path: str, die_name: str) -> pd.DataFrame:
    """Load a C4 CSV file (x, y, net) and attach die name."""
    df = pd.read_csv(path)
    required = {"x", "y", "net"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"{path} missing required columns: {missing}")

    df = df.copy()
    df["die"] = die_name
    return df


def apply_mapping(df: pd.DataFrame, prefix: str, global_nets: set) -> pd.DataFrame:
    """Apply prefix mapping to net names except global nets."""
    def map_net(net: str) -> str:
        if net in global_nets:
            return net
        return prefix + net

    out = df.copy()
    out["net_mapped"] = out["net"].apply(map_net)
    return out


def run_mapping(config_path: str, override_output: str | None = None):
    """Process all dies and write separate mapped CSV files."""
    project_root = os.path.dirname(os.path.abspath(config_path))

    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)

    dies_cfg = cfg.get("dies", [])
    global_nets = set(cfg.get("global_nets", []))

    if not dies_cfg:
        raise ValueError("dies section in config is empty")

    # Determine output directory
    if override_output:
        out_dir = override_output
    else:
        out_dir = cfg.get("output", {}).get("dir", "out")

    abs_out_dir = os.path.join(project_root, out_dir)
    os.makedirs(abs_out_dir, exist_ok=True)

    # Process each die individually
    for die_cfg in dies_cfg:
        die_name = die_cfg["name"]
        prefix = die_cfg["prefix"]
        rel_file = die_cfg["file"]

        in_path = os.path.join(project_root, rel_file)
        if not os.path.exists(in_path):
            raise FileNotFoundError(f"{in_path} not found")

        df_raw = load_c4(in_path, die_name)
        df_mapped = apply_mapping(df_raw, prefix, global_nets)

        # Add PIN_NUMBER per-die (local unique numbering)
        df_mapped = df_mapped.reset_index(drop=True)
        df_mapped["PIN_NUMBER"] = df_mapped.index + 1

        # Output file name: e.g., out/DIE0_mapped.csv
        out_file = os.path.join(abs_out_dir, f"{die_name}_mapped.csv")
        df_mapped.to_csv(out_file, index=False)

        print(f"Wrote {len(df_mapped)} rows to {out_file}")


def main():
    parser = argparse.ArgumentParser(description="Multi-die C4 net mapping tool")
    parser.add_argument(
        "-c",
        "--config",
        default="mapping_config.yaml",
        help="Path to mapping_config.yaml",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Override output directory (optional)",
    )
    args = parser.parse_args()

    run_mapping(args.config, args.output)


if __name__ == "__main__":
    main()
