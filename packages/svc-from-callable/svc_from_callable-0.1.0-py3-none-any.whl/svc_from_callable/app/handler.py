"""handler.py."""
import logging

from strangeworks_core.errors.error import StrangeworksError
from sw_product_lib import service
from sw_product_lib.service import RequestContext
from sw_product_lib.types.job import Job, JobStatus

from . import AppFunction
from .types import SubmitRequest


def execute_request(
    ctx: RequestContext, app_fn: AppFunction, submit_request: SubmitRequest
) -> Job:
    """Execute Callable Request."""
    # Even if the job submission fails, there should be a record of it on the platform.
    sw_job: Job = service.create_job(ctx)

    # TODO: add estimate cost here.

    try:
        logging.info(f"executing job request (job slug: {sw_job.slug})")
        result = app_fn(**submit_request.callable_params)
        logging.info(f"uploading job result (job slug: {sw_job.slug})")
        service.upload_job_artifact(
            result,
            ctx=ctx,
            job_slug=sw_job.slug,
            file_name="result.json",
        )
        logging.info(f"updating job status to COMPLETED (job slug: {sw_job.slug})")
        service.update_job(
            ctx=ctx,
            job_slug=sw_job.slug,
            status=JobStatus.COMPLETED,
        )
        # TODO: add billing transaction here.
        logging.info(f"completed execution of job request (job slug: {sw_job.slug})")
    except Exception as err:
        service.update_job(
            ctx=ctx,
            job_slug=sw_job.slug,
            status=JobStatus.FAILED,
        )
        raise StrangeworksError(message=err) from err

    return sw_job
