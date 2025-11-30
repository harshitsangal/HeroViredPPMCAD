#!/usr/bin/env python3
import time
import sys
import argparse
import logging
import psutil
from typing import Optional

def setup_logger(log_file: Optional[str] = None, level: int = logging.INFO):
    """
    Configure logger: output to console and optionally to a file.
    """
    logger = logging.getLogger("cpu_monitor")
    logger.setLevel(level)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    if log_file:
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

def monitor_cpu(threshold: float = 80.0,
                interval: float = 1.0,
                per_core: bool = False,
                log_file: Optional[str] = None):
    """
    Keep watching CPU usage. If usage crosses threshold, log a warning.
    Runs until interrupted by user or error.
    """
    logger = setup_logger(log_file)
    logger.info(f"CPU monitor started (threshold={threshold}%, interval={interval}s, per_core={per_core})")

    try:
        while True:
            total = psutil.cpu_percent(interval=interval)
            cores = psutil.cpu_percent(interval=0.0, percpu=True) if per_core else None

            msg = f"CPU total: {total:.1f}%"
            if cores is not None:
                core_states = ", ".join(f"core{i}: {pct:.1f}%" for i, pct in enumerate(cores))
                msg += f" | {core_states}"

            logger.info(msg)

            if total > threshold:
                logger.warning(f"ALERT: CPU usage above threshold — {total:.1f}%")

    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user. Exiting.")
    except Exception as e:
        logger.error("Unexpected error during monitoring", exc_info=True)
        sys.exit(1)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Monitor CPU usage and alert on high load."
    )
    parser.add_argument('-t', '--threshold', type=float, default=80.0,
                        help='Usage % to trigger alert (default: 80.0)')
    parser.add_argument('-i', '--interval', type=float, default=1.0,
                        help='Seconds between checks (default: 1.0)')
    parser.add_argument('-p', '--per-core', action='store_true',
                        help='Also report per-core usage')
    parser.add_argument('-l', '--log-file', type=str, default=None,
                        help='Optional log file path')
    return parser.parse_args()

def main():
    args = parse_args()
    monitor_cpu(threshold=args.threshold,
                interval=args.interval,
                per_core=args.per_core,
                log_file=args.log_file)

if __name__ == "__main__":
    main()
