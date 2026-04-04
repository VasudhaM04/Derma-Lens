from pathlib import Path
import torch


def export_to_onnx(model, output_path, input_size=(1, 3, 224, 224), opset_version=17):
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    dummy = torch.randn(*input_size)
    model.eval()
    torch.onnx.export(
        model,
        dummy,
        str(output),
        opset_version=opset_version,
        input_names=["input"],
        output_names=["risk_logits"],
        dynamic_axes={"input": {0: "batch"}, "risk_logits": {0: "batch"}},
    )
    return output
