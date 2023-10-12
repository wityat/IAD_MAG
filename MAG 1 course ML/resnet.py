import torch
import torch.nn as nn


class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=(3, 3), stride=(1, 1), padding=1, bias=False)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=(3, 3), stride=(1, 1), padding=1, bias=False)

        self.shortcut = nn.Sequential()
        if in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=(3, 3), stride=(1, 1), padding=1, bias=False)
            )

    def forward(self, x):
        residual = self.shortcut(x)

        out = self.conv1(x)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.relu(out)

        out += residual

        return out


# Определение ResNet
class ResNet(nn.Module):
    def __init__(self):
        super(ResNet, self).__init__()
        self.conv1 = nn.Conv2d(3, 64, kernel_size=(7, 7), stride=(1, 1), padding=1, bias=False)
        self.relu = nn.ReLU(inplace=True)
        self.pool1 = nn.MaxPool2d(kernel_size=(3, 3))

        self.res_block1 = ResidualBlock(64, 64)
        self.res_block2 = ResidualBlock(64, 64)
        self.res_block3 = ResidualBlock(64, 128)

        self.res_block4 = ResidualBlock(128, 128)
        self.res_block5 = ResidualBlock(128, 128)
        self.res_block6 = ResidualBlock(128, 512)

        self.res_block7 = ResidualBlock(512, 512)
        self.res_block8 = ResidualBlock(512, 512)
        self.res_block9 = ResidualBlock(512, 512)

        self.pool2 = nn.MaxPool2d(kernel_size=(3, 3))
        self.fc_1000 = nn.Linear(16005632, 1000)
        self.soft_max = nn.Softmax()

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.pool1(x)
        x = self.res_block1(x)
        x = self.res_block2(x)
        x = self.res_block3(x)

        x = self.res_block4(x)
        x = self.res_block5(x)
        x = self.res_block6(x)

        x = self.res_block7(x)
        x = self.res_block8(x)
        x = self.res_block9(x)

        x = self.pool2(x)
        x = torch.flatten(x)
        x = self.fc_1000(x)
        x = self.soft_max(x)
        return x


model = ResNet()

x = torch.rand([1, 3, 16, 16])

y = model.forward(x)
print(y.shape)
target = torch.tensor([[[2]]], dtype=torch.long)


criterion = nn.CrossEntropyLoss()
loss = criterion(y, target)
loss.backward()
