from fastapi import APIRouter, HTTPException, status
from typing import Union, List
from app.models.models import TFBSRequest, TFBSWindow, TFBSDetail
from app.utils.pwm import search_luncher
from app.utils.utils import Entrez
import traceback

router = APIRouter()


@router.post("/tfbs", response_model=Union[List[TFBSWindow], dict], status_code=200)
def get_tfbs(request: TFBSRequest):
    try:
        Entrez.email = request.email

        if not request.m or not request.mrna:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Motif and mRNA parameters are required",
            )

        tf_name, wsi = search_luncher(
            request.mrna,
            request.m,
            request.p,
            request.t,
            request.l,
            request.w,
            request.s,
        )

        if len(wsi) == 0:
            return {
                "message": "No TFBS found with these parameters, please choose different ones",
                "parameters": {
                    "motif": request.m,
                    "threshold": request.t,
                    "promoter_length": request.l,
                    "window_size": request.w,
                    "window_threshold": request.s,
                    "pseudocount": request.p,
                    "mrna": request.mrna,
                },
            }

        output = []
        for i in wsi:
            window_info = TFBSWindow(
                window_id=int(i),
                tf=tf_name,
                window_pos=[int(wsi[i][0]), int(wsi[i][1])],
                window_score=float(wsi[i][2]),
                details=[
                    TFBSDetail(
                        sequence_id=j,
                        position=int(wsi[i][3][j][0]),
                        score=float(wsi[i][3][j][1]),
                    )
                    for j in wsi[i][3]
                ],
            )
            output.append(window_info)

        return output

    except Exception as e:
        traceback_str = "".join(traceback.format_tb(e.__traceback__))
        error_message = f"{str(e)}\n{traceback_str}"
        print(f"Exception: {error_message}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred. Please try again later.",
        )
