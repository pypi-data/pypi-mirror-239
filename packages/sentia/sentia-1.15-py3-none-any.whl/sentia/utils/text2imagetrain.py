import argparse
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoTokenizer, CLIPTextModel
from torchvision import transforms
from PIL import Image
from sentia.modeling_sentia import SENTIAConfig, SENTIAForImageGeneration
import requests
from io import BytesIO
from datasets import load_dataset
import matplotlib.pyplot as plt

torch.manual_seed(1024)
torch.cuda.manual_seed(1024)
# Define your custom dataset
class CustomImageTextDataset(Dataset):
    def __init__(self, tokenizer, data, transform=None):
        self.tokenizer = tokenizer
        self.data = data
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        text = item['prompt']
        image_path = item['image']

        # Load and preprocess the image
        if isinstance(image_path, str):
            if image_path.startswith("http"):
                response = requests.get(image_path)
                image = Image.open(BytesIO(response.content))
            else:
                image = Image.open(image_path)
        else:
            image = image_path

        if self.transform:
            image = self.transform(image).to("cuda", dtype=torch.float32)
            image = torch.flatten(image)

        # Tokenize the text
        inputs = self.tokenizer(text, return_tensors='pt', padding='max_length', max_length=48, truncation=True)

        return {
            'input_ids': inputs['input_ids'].to("cuda"),
            'labels': image
        }


def train(args):
    # Initialize the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.pretrained_model)
    config = SENTIAConfig(len(tokenizer), args.hidden_dim, n_embed=args.embedding_dim, n_layer=args.num_layers, n_head=args.num_heads, pad_token_id=tokenizer.pad_token_id)
    model = SENTIAForImageGeneration(config, discriminator=None, add_latent=False, discriminator_weight=0.5)
    model.summary()
    model.to("cuda", dtype=torch.float32)
    optimizer = torch.optim.RMSprop(model.parameters(), lr=3e-4, momentum=0.5)
    # Define the dataset with image URLs and text data
    data = load_dataset("poloclub/diffusiondb", "2m_first_10k", split="train")
    # Define the dataset and dataloader
    transform = transforms.Compose([
        transforms.Resize((512, 512)),
        transforms.ToTensor(),
    ])

    dataset = CustomImageTextDataset(tokenizer, data, transform=transform)
    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True)

    # Training loop (remaining part remains the same)
    for epoch in range(args.num_epochs):
        model.train()
        total_loss = 0

        for i, batch in enumerate(dataloader):

            optimizer.zero_grad()
            outputs = model(**batch)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            print(f"Batch {i}/{len(dataloader)} - Loss: {loss.item()}")

            total_loss += loss.item()
            if i == 2499:
                generated_image = outputs.image_outputs
                generated_image = generated_image[0, 0, 0, :]
                generated_image = generated_image.view(512, 512, 3).detach().cpu().numpy()
                image = Image.fromarray((generated_image * 255).astype("uint8"))
                image.show()

        average_loss = total_loss / len(dataloader)
        print(f'Epoch [{epoch + 1}/{args.num_epochs}] Loss: {average_loss:.4f}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--pretrained_model', type=str, default='Locutusque/gpt2-xl-conversational')
    parser.add_argument('--hidden_dim', type=int, default=2048)
    parser.add_argument('--embedding_dim', type=int, default=2048)
    parser.add_argument('--num_layers', type=int, default=72)
    parser.add_argument('--num_heads', type=int, default=64)
    parser.add_argument('--batch_size', type=int, default=4)
    parser.add_argument('--num_epochs', type=int, default=20)

    args = parser.parse_args()
    train(args)
