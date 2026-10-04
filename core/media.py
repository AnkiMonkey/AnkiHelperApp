"""Bezpečné kopírovanie/presun obrázkov (napr. do collection.media).

Pred akciou sa vytvorí plán:
  new       – súbor v cieli ešte nie je
  identical – v cieli je presne ten istý súbor (preskočí sa)
  changed   – v cieli je súbor s rovnakým menom, ale INÝM obsahom
              (prepíše sa až po potvrdení)
"""

import filecmp
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from . import IMAGE_EXTENSIONS


@dataclass
class TransferPlan:
    destination: Path
    new: list = field(default_factory=list)
    identical: list = field(default_factory=list)
    changed: list = field(default_factory=list)

    @property
    def total(self):
        return len(self.new) + len(self.identical) + len(self.changed)


def image_files(folder):
    return sorted(
        (path for path in Path(folder).iterdir() if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS),
        key=lambda path: path.name.lower(),
    )


def plan_transfer(files, destination):
    destination = Path(destination)
    plan = TransferPlan(destination=destination)
    for source in files:
        target = destination / source.name
        if not target.exists():
            plan.new.append(source)
        elif filecmp.cmp(source, target, shallow=False):
            plan.identical.append(source)
        else:
            plan.changed.append(source)
    return plan


def execute_transfer(plan, move=False, overwrite_changed=True):
    """Vráti počet spracovaných súborov. Identické súbory sa neprepisujú."""
    plan.destination.mkdir(parents=True, exist_ok=True)
    to_process = list(plan.new)
    if overwrite_changed:
        to_process += plan.changed

    done = 0
    for source in to_process:
        target = plan.destination / source.name
        if move:
            shutil.move(str(source), str(target))
        else:
            shutil.copy2(source, target)
        done += 1

    if move:
        # identický súbor už v cieli je – zdroj je len duplikát
        for source in plan.identical:
            source.unlink()
    return done


def describe_plan(plan, limit=15):
    lines = [
        f"Nové: {len(plan.new)}",
        f"Rovnaké (preskočím): {len(plan.identical)}",
        f"S rovnakým menom, iný obsah (prepíšem): {len(plan.changed)}",
    ]
    if plan.changed:
        lines.append("")
        lines += [f"  • {path.name}" for path in plan.changed[:limit]]
        if len(plan.changed) > limit:
            lines.append(f"  … a ďalších {len(plan.changed) - limit}")
    return "\n".join(lines)
