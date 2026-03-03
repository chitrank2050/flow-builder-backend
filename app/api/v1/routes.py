from fastapi import APIRouter

from app.schemas import PipelineRequest, PipelineResponse
from app.services import is_dag

router = APIRouter()


@router.post(
    "/pipelines/parse",
    response_model=PipelineResponse,
    name="Parse the pipeline",
)
def parse_pipeline(pipeline: PipelineRequest) -> PipelineResponse:
    return PipelineResponse(
        num_nodes=len(pipeline.nodes),
        num_edges=len(pipeline.edges),
        is_dag=is_dag(pipeline.nodes, pipeline.edges),
    )
