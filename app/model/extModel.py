import torch
import torchvision.models as models

from config.config import CgdConfig
from app.model.cgd import *

class Resnet18():
    def __init__(self):
        self.model = models.resnet18(pretrained=True)
        self.FE = torch.nn.Sequential(*list(self.model.children())[:-1])
        print("[RESNET18] Loading Resnet18 vector extractor Model...")


class Cgd:
    def __init__(self):
        # define model params
        self.cgdName = CgdConfig.MODEL_NUM
        self.model_params = {}
        self.model_params['architecture'] = CgdConfig.ARCHITECTURE
        self.model_params['output_dim'] = CgdConfig.OUTPUT_DIM
        self.model_params['combination'] = CgdConfig.COMBINATION
        self.model_params['pretrained'] = CgdConfig.PRETRAINED
        self.model_params['classes'] = CgdConfig.CLASSES

        # define device
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # define model and weight
        self.weight = torch.load(f'{CgdConfig.WEIGHTDIR}model{self.cgdName}_best.pth.tar')
        self.model =  init_network(self.model_params).to(self.device)
        self.model.load_state_dict(self.weight['state_dict'])

        print(f'[CGD{self.cgdName}] Loading CGD{self.cgdName} vector extractor Model...')
    

    def featureExt(self, inputVec):
        # load model & image on cuda
        self.model.cuda(), self.model.eval()
        inputVec = inputVec.cuda()

        # extract vecs
        extVecs = self.model(inputVec)[0].cpu().squeeze()

        torch.cuda.empty_cache()

        return extVecs









