from fastapi import APIRouter

from app.dataBase import MySQL
from app.vector.extVector import Vector
from app.faissLib.extFaiss import FaissLib
from app.vector import utils as util

import time

# define router
router = APIRouter()

# difine class
VEC = Vector()
faisss = FaissLib()


@router.put('/test')
async def createFaiss():
    cate, num, writeM = "WC13", 500, "w"

    flist = MySQL.getImgList(cate, num)
    yoloResult = VEC.getYoloBox(flist)

    for key in yoloResult['info'].keys():
        if not key == "Dress": continue
        count = len(yoloResult['info'][key])
        st_time = time.time()
        

        # Save INFO
        util.saveInfos(yoloResult['info'][key], key, writeM)
        
        tensorStack = VEC.changePILtoTensorStack(yoloResult['vecs'][key])
        extVecs = VEC.extractVec(tensorStack) # Take Time
        util.saveVecs(extVecs, key, writeM)

        # # create Faiss Index
        faisss.writeIndexFile(key)
        
        endTime = time.time()-st_time

        print(f'[{key}] count : {count} & time : {endTime}')
        del st_time, endTime, count, tensorStack, extVecs