# chiplet-net-mapper

A lightweight and transparent open-source tool for mapping and prefixing C4 bump nets in multi-die chiplet designs.

The tool reads simple per-die C4 maps (`x, y, net`) and generates consistently renamed, per-die mapped CSV files with unique pin numbering — ready for downstream EDA/package flows (APD/SIP/Allegro/etc.).
The goal is to provide a clean, automatable foundation for chiplet and multi-die integration.

---

## Features (OSS Core)

- **Per-die C4 CSV input**
  - Minimal format: `x, y, net`
- **Automatic net renaming with prefixes**
  - Example: `RF_IN0_P` → `d0_RF_IN0_P`
- **Global net passthrough**
  - `VSS`, `VDD`, `AGND`, etc. remain unchanged
- **Per-die output CSV files**
  - Example: `out/DIE0_mapped.csv`, `out/DIE1_mapped.csv`
- **Unique per-die `PIN_NUMBER` generation**
- **Configurable via simple YAML**
- **Zero external EDA dependencies**

This repository focuses on clarity, reproducibility, and easy integration into real packaging flows.

---

## Project Structure

chiplet-net-mapper/
│
├── chipnet.py             # main CLI script
├── mapping_config.yaml    # configuration file
├── data/
│   ├── DIE0_c4.csv
│   └── DIE1_c4.csv
└── out/
    └── (generated files)

---

## Input Format (per-die C4 map)

Each die's C4 map is kept intentionally simple:

x,y,net
10,90,RF_IN0_P
10,85,RF_IN0_N
20,50,GPIO_CLK
5,5,VSS

No layers, types, directions, or ESD info — the focus is purely geometric + logical net naming.

---

## Configuration (`mapping_config.yaml`)

dies:
  - name: DIE0
    prefix: d0_
    file: data/DIE0_c4.csv

  - name: DIE1
    prefix: d1_
    file: data/DIE1_c4.csv

global_nets:
  - VSS
  - VSSH
  - AGND
  - VDD
  - AVDD1
  - AVDD2

rules: []   # (reserved for future renaming rules)

output:
  dir: out

---

## Usage

Install dependencies:

pip install -r requirements.txt

Run the mapper:

python chipnet.py -c mapping_config.yaml

Output files appear under:

out/DIE0_mapped.csv
out/DIE1_mapped.csv

---

## Output Example

x,y,net,die,net_mapped,PIN_NUMBER
10,90,RF_IN0_P,DIE0,d0_RF_IN0_P,1
10,85,RF_IN0_N,DIE0,d0_RF_IN0_N,2
5,5,VSS,DIE0,VSS,3

---

## Roadmap (Open-Source Core)

Planned enhancements include:

- Regex-based renaming rules
- Improved error/consistency checking
- Sorting and custom mapping options
- Extended test dataset

The core functionality will always remain free and open-source.

---

## Planned Pro Edition (Future)

A separate Pro edition is planned with advanced capabilities such as:

- C4 / netlist diff comparison
- Unified package-level net generation
- Auto grouping (P/N pairs, RF/HSS/etc.)
- HTML/PDF visual reports
- Die-to-die consistency checks
- P/N pairing and grouping automation
- Cadence APD/SIP & Allegro export helpers (SKILL/TCL/CSV)
- Batch mode & CI/CD integration

These features are relevant to production-level multi-die/advanced packaging flows.

---

## Contributing

Issues, suggestions, and pull requests are welcome.
The aim is to keep the codebase simple, readable, and easy to extend.

---

## License

MIT License.

---

## Note

This project is an independent open-source effort created outside of any employer.
It uses no proprietary data, formats, or confidential information.
