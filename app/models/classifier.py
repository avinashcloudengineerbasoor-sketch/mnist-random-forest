import torch
import torch.nn as nn


class FinalClassifier(nn.Module):

    def __init__(self, image_feat_dim=128, metadata_dim=6, num_classes=10):
        super().__init__()

        self.fc = nn.Sequential(
            nn.Linear(image_feat_dim + metadata_dim, 64),
            nn.ReLU(),
            nn.Linear(64, num_classes),
        )

    def forward(self, img_feat, meta_feat):
        return self.fc(torch.cat([img_feat, meta_feat], dim=1))
