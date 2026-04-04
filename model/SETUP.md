# DermaLens — FairDermNet: Setup Notes

## Python Environment

The project requires **Python 3.10** specifically, because:
- PyTorch 2.0+ CUDA wheels are built against Python 3.10 on this machine.
- TensorFlow 2.13 has limited support outside 3.8–3.11, and 3.10 is the tested version.
- Newer Python versions (3.11+) have caused CUDA initialisation failures in testing.

Install dependencies into your Python 3.10 environment:

```bash
pip install -r requirements.txt
```

---

## Jupyter Kernel Fix (IMPORTANT — read before running the notebook)

If you open `notebooks/dermalens_train.ipynb` and hit a **CUDA not found**, **module not found**, or **wrong Python** error, the issue is almost certainly the Jupyter kernel pointing at the wrong interpreter.

The notebook must run under the **Python 3.10** kernel tied to:

```
C:\Users\sanja\AppData\Local\Programs\Python\Python310\python.exe
```

### To fix permanently

1. Register a dedicated IPython kernel for this interpreter:

```bash
C:\Users\sanja\AppData\Local\Programs\Python\Python310\python.exe -m ipykernel install --user --name dermalens-py310 --display-name "DermaLens (Python 3.10)"
```

2. In Jupyter / VS Code, switch the notebook kernel to **"DermaLens (Python 3.10)"**.

3. Verify inside the notebook:

```python
import sys
print(sys.executable)   # should be …\Python310\python.exe
import torch
print(torch.cuda.is_available())   # should be True if CUDA drivers are installed
```

If you need to edit the kernel spec directly, it lives at:

```
C:\Users\sanja\AppData\Roaming\jupyter\kernels\dermalens-py310\kernel.json
```

The critical field is:

```json
{
  "argv": [
    "C:\\Users\\sanja\\AppData\\Local\\Programs\\Python\\Python310\\python.exe",
    "-m", "ipykernel_launcher", "-f", "{connection_file}"
  ],
  "display_name": "DermaLens (Python 3.10)",
  "language": "python"
}
```

---

## Known TODOs / Inaccuracies to Fix Post-Training

| Item | Detail |
|---|---|
| **Notebook cell count** | The notebook has **15 cells** (Cells 9b and 9c were added as part of the multiclass patch for DDI held-out eval and clinical threshold analysis). Any documentation still saying "13 cells" is stale. |
| **Parameter count** | "~5.4M parameters, ~5.8 MB quantized" is an estimate based on vanilla MobileNetV3-Large. The `FairnessAttentionModule` (channel attention, spatial attention, cross-attention modulator, Fitzpatrick auxiliary branch) adds parameters on top of the backbone. Re-verify the exact count and quantized file size after the first successful training run by checking the ONNX export size and running `sum(p.numel() for p in model.parameters())`. |

---

## Quick-Start

```bash
# 1. Clone / open the project
cd "path/to/model"

# 2. Install dependencies (Python 3.10 only)
C:\Users\sanja\AppData\Local\Programs\Python\Python310\python.exe -m pip install -r requirements.txt

# 3. Register the Jupyter kernel (one-time)
C:\Users\sanja\AppData\Local\Programs\Python\Python310\python.exe -m ipykernel install --user --name dermalens-py310 --display-name "DermaLens (Python 3.10)"

# 4. Open the notebook and select the "DermaLens (Python 3.10)" kernel
# notebooks/dermalens_train.ipynb
```

Run cells top-to-bottom. Cell 1 will confirm your GPU is visible before any heavy work begins.
