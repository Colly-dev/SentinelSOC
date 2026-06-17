# SentinelSOC Architecture

SentinelSOC is designed as a modular Security Operations Center (SOC) simulation platform.

## Core Components

1.  **Collectors**: Modules responsible for gathering logs from various sources (Windows, Linux, Sysmon, etc.).
2.  **Normalizer**: Converts raw logs into a common schema (SentinelSOC Common Schema).
3.  **Detection Engine**: Applies logic to normalized events to identify suspicious patterns.
4.  **Alert Manager**: Handles alert lifecycle, storage, and severity classification.
5.  **Correlation Engine**: Groups related alerts into higher-level incidents based on common attributes (IP, User, Time).
6.  **Report Engine**: Generates human-readable and machine-parseable reports (HTML, JSON, CSV).

## Data Flow

```mermaid
graph LR
    A[Log Sources] --> B[Collectors]
    B --> C[Normalizer]
    C --> D[Detection Engine]
    D --> E[Alert Manager]
    E --> F[Correlation Engine]
    F --> G[Report Engine]
    G --> H[Output Reports]
```
