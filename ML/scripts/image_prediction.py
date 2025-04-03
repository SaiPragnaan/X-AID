import torchvision
from torchvision.models import mobilenet_v3_large
import os
import torch
import torch.nn as nn
from torchvision.transforms import v2
from PIL import Image

classifier=nn.Sequential(
    nn.Dropout(p=0.2,inplace=True),
    nn.Linear(in_features=960,out_features=256),
    nn.Linear(in_features=256,out_features=64),
    nn.Linear(in_features=64,out_features=16),
    nn.Linear(in_features=16,out_features=8),
    nn.Linear(in_features=8,out_features=2),
).to('cpu')

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "mobilenetv3_model.pth")
model = mobilenet_v3_large(weights=None) 
model.classifier=classifier
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))

print("Model loaded successfully!")
# print(torch.__version__)

transforms = v2.Compose([
    v2.ToImage(),  
    v2.ToDtype(torch.float32, scale=True),  
    v2.Grayscale(num_output_channels=3),  

    v2.Resize((224, 224)),

    v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  
])

def predict(img):
    # img=Image.open(image_path)
    image=transforms(img)
    if len(image.shape) == 3:  
        image = image.unsqueeze(0)  

    model.eval()

    with torch.no_grad():
        output = model(image)
        predicted_class = torch.argmax(output, dim=1).item()

    if predicted_class == 1:
        return (
            "🔴 Potential pneumonia detected. The model indicates a high probability of pneumonia in this X-ray scan.It is recommended to consult a medical professional for further evaluation and confirmatory tests. Early diagnosis and treatment are important for better health outcomes."
        )
    else:
        return (
            "🟢 Lungs appear normal. Based on the analysis, there are no significant signs of pneumonia in this scan. However, if you experience symptoms like cough, fever, chest pain, or difficulty breathing, please consult a doctor for further evaluation. Regular health check-ups are always recommended."
        )
