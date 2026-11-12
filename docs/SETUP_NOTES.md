# Local setup notes (Intel Mac, macOS 11 Big Sur)

These notes explain setup choices that differ from a "standard" install.

| Issue | Decision | Why |
|---|---|---|
| No `pyarrow` wheel for Intel macOS 11 + Python 3.13 | Use `fastparquet` for Parquet | pandas picks it automatically for `to_parquet` / `read_parquet`; no compiler needed |
| LightGBM needs OpenMP (`libomp.dylib`) at import | `brew install libomp` | LightGBM's wheel looks in `/usr/local/opt/libomp/lib`; installed by name so `brew autoremove` keeps it |
| Homebrew auto-removed its Python 3.13, breaking `.venv` | Reinstalled `python@3.13` by name and ran `brew pin python@3.13` | Formulae installed by name are not auto-removed; pinning prevents upgrades from moving Python under the venv |
| Plain `python3` is Apple's 3.8.2 | Create the venv with the full path `/usr/local/opt/python@3.13/bin/python3.13 -m venv .venv` | Avoids changing the system `python3`; inside `(.venv)`, `python` is always 3.13 |
| Unpinned `>=` requirements | `requirements-ml.lock.txt` from `pip freeze` | Reproducible training and SHAP results |

## Rebuild the environment
    rm -rf .venv
    /usr/local/opt/python@3.13/bin/python3.13 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    pip install -r requirements-ml.lock.txt

## Do not
- Run `brew upgrade` without checking whether it touches `python@3.13` (it should be pinned).