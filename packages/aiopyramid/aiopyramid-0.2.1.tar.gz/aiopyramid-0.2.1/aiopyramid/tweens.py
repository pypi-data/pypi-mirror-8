import greenlet
import asyncio
import logging

log = logging.getLogger(__name__)


def coroutine_logger_tween_factory(handler, registry):
    """
    Example of an asyncronous tween that delegates a syncronous function to
    a child thread. This tween asyncronously logs all requests and responses.
    """

    @asyncio.coroutine
    def _async_log(back, content):
        # log doesn't really need to be run in a separate thread
        # but it works for demonstration purposes
        # NOTE: this does not do exception handling, which means
        # that no 500 error view will be run. The exception needs to
        # be reraised in the request greenlet. See helpers.run_in_greenlet for
        # and example.

        yield from asyncio.get_event_loop().run_in_executor(
            None,
            log.info,
            content
        )
        back.switch()

    def coroutine_logger_tween(request):
        # get this greenlet
        this = greenlet.getcurrent()

        # queue request logging
        sub_task = asyncio.async(_async_log(this, request))

        # switch to parent so that aio loop runs
        # (waiting for subtask if gunicorn)
        this.parent.switch(sub_task)

        # when request is logged, it will switch back to this

        # get response, this could also be done in a coroutine
        response = handler(request)

        # queue respone logging
        sub_task = asyncio.async(_async_log(this, response))

        # switch to parent so that aio loop runs
        # (waiting for subtask if gunicorn)
        this.parent.switch(sub_task)

        # when response is logged, it will switch back to this

        # return response after logging is done
        return response

    return coroutine_logger_tween
