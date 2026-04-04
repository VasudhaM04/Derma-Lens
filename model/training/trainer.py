from typing import Dict

import torch


def build_optimizer(model, config: Dict):
    lr = config["training"]["learning_rate"]
    weight_decay = config["training"]["weight_decay"]
    return torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)


def build_scheduler(optimizer, config: Dict):
    epochs = config["training"]["epochs"]
    return torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
        optimizer,
        T_0=max(1, epochs // 5),
        T_mult=1,
    )


def training_step(model, batch, criterion, device):
    images, risk_labels, tone_labels = batch
    images = images.to(device)
    risk_labels = risk_labels.to(device)
    tone_labels = tone_labels.to(device)

    risk_logits, tone_logits = model(images)
    loss = criterion(risk_logits, tone_logits, risk_labels, tone_labels)
    return loss, risk_logits, tone_logits
