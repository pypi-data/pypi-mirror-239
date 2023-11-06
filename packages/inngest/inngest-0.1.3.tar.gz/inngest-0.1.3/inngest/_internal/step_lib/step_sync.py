import datetime
import typing

from inngest._internal import event_lib, execution, transforms, types

from . import base


class StepSync(base.StepBase):
    def run(
        self,
        step_id: str,
        handler: typing.Callable[[], types.SerializableT],
    ) -> types.SerializableT:
        """
        Run logic that should be retried on error and memoized after success.

        Args:
        ----
            step_id: Durable step ID. Should usually be unique within a
                function, but it's OK to reuse as long as your function is
                deterministic.
            handler: The logic to run.
        """
        hashed_id = self._get_hashed_id(step_id)

        memo = self.get_memo_sync(hashed_id)
        if memo is not types.EmptySentinel:
            return memo  # type: ignore

        err = self._middleware.before_execution_sync()
        if isinstance(err, Exception):
            raise err

        raise base.Interrupt(
            hashed_id=hashed_id,
            data=handler(),
            display_name=step_id,
            op=execution.Opcode.STEP,
            name=step_id,
        )

    def send_event(
        self,
        step_id: str,
        events: event_lib.Event | list[event_lib.Event],
    ) -> list[str]:
        """
        Send an event or list of events.

        Args:
        ----
            step_id: Durable step ID. Should usually be unique within a
                function, but it's OK to reuse as long as your function is
                deterministic.
            events: An event or list of events to send.
        """

        def fn() -> list[str]:
            return self._client.send_sync(events)

        return self.run(step_id, fn)

    def sleep(
        self,
        step_id: str,
        duration: int | datetime.timedelta,
    ) -> None:
        """
        Sleep for a duration.

        Args:
        ----
            step_id: Durable step ID. Should usually be unique within a
                function, but it's OK to reuse as long as your function is
                deterministic.
            duration: The number of milliseconds to sleep.
        """
        if isinstance(duration, int):
            until = datetime.datetime.utcnow() + datetime.timedelta(
                milliseconds=duration
            )
        else:
            until = datetime.datetime.utcnow() + duration

        return self.sleep_until(step_id, until)

    def sleep_until(
        self,
        step_id: str,
        until: datetime.datetime,
    ) -> None:
        """
        Sleep until a specific time.

        Args:
        ----
            step_id: Durable step ID. Should usually be unique within a
                function, but it's OK to reuse as long as your function is
                deterministic.
            until: The time to sleep until.
        """
        hashed_id = self._get_hashed_id(step_id)

        memo = self.get_memo_sync(hashed_id)
        if memo is not types.EmptySentinel:
            return memo  # type: ignore

        err = self._middleware.before_execution_sync()
        if isinstance(err, Exception):
            raise err

        raise base.Interrupt(
            hashed_id=hashed_id,
            display_name=step_id,
            name=transforms.to_iso_utc(until),
            op=execution.Opcode.SLEEP,
        )

    def wait_for_event(
        self,
        step_id: str,
        *,
        event: str,
        if_exp: str | None = None,
        timeout: int | datetime.timedelta,
    ) -> event_lib.Event | None:
        """
        Wait for an event to be sent.

        Args:
        ----
            step_id: Durable step ID. Should usually be unique within a
                function, but it's OK to reuse as long as your function is
                deterministic.
            event: Event name.
            if_exp: An expression to filter events.
            timeout: The maximum number of milliseconds to wait for the event.
        """
        hashed_id = self._get_hashed_id(step_id)

        memo = self.get_memo_sync(hashed_id)
        if memo is not types.EmptySentinel:
            if memo is None:
                # Timeout
                return None

            # Fulfilled by an event
            return event_lib.Event.model_validate(memo)

        err = self._middleware.before_execution_sync()
        if isinstance(err, Exception):
            raise err

        timeout_str = transforms.to_duration_str(timeout)
        if isinstance(timeout_str, Exception):
            raise timeout_str

        opts = base.WaitForEventOpts(
            if_exp=if_exp,
            timeout=timeout_str,
        ).to_dict()
        if isinstance(opts, Exception):
            raise opts

        raise base.Interrupt(
            hashed_id=hashed_id,
            display_name=step_id,
            name=event,
            op=execution.Opcode.WAIT_FOR_EVENT,
            opts=opts,
        )
