from pathlib import Path
from setuptools import find_packages, setup


ROOT = Path(__file__).resolve().parent


def read_requirements() -> list:
    req_path = ROOT / "requirements.txt"
    if not req_path.exists():
        return []
    return [line.strip() for line in req_path.read_text(encoding="utf-8").splitlines() if line.strip()]


setup(
    name="dermalens-fairdermnet",
    version="0.1.0",
    description="DermaLens fairness-aware, explainable skin cancer risk model pipeline.",
    packages=find_packages(exclude=("notebooks", "datasets")),
    include_package_data=True,
    install_requires=read_requirements(),
    python_requires=">=3.8",
)
