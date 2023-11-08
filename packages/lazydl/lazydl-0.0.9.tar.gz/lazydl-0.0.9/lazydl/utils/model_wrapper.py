import lightning.pytorch as pl
import torch


class LightningModel(pl.LightningModule):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, input_ids, attention_mask, target, *args, **kwargs):
        return self.model(input_ids, attention_mask, target)

    def training_step(self, batch, batch_idx):
        output = self(**batch)
        loss = self.compute_loss(output, batch["target"])
        return loss
    
    def compute_loss(self, outputs, labels):
        return torch.nn.functional.nll_loss(outputs, labels.view(-1))

    def configure_optimizers(self):
        return torch.optim.SGD(self.model.parameters(), lr=0.1)