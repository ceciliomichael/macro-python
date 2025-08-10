import threading
import time
from datetime import datetime, timedelta, time as dt_time
from typing import Any, Callable, Dict, List, Optional


class MacroScheduler:
    """Lightweight scheduler to trigger macro playback at configured times.

    Supports schedule types: once (datetime), daily (time), weekly (time + days), interval (seconds).
    Thread-safe and UI-thread friendly via a provided controller with tk.after().
    """

    def __init__(self, controller):
        # controller is MacroRecorderGUI, must expose: root (tk), is_playing, start_auto_playback(), update_status(str)
        self.controller = controller
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self.enabled: bool = False
        self.schedules: List[Dict[str, Any]] = []
        self._next_run_cache: Dict[str, Optional[datetime]] = {}
        self._check_interval_seconds: float = 1.0

    # ---------------- Public API ---------------- #
    def start(self) -> None:
        with self._lock:
            if self._thread and self._thread.is_alive():
                return
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._run_loop, name="MacroSchedulerThread", daemon=True)
            self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        thread = None
        with self._lock:
            thread = self._thread
            self._thread = None
        if thread and thread.is_alive():
            thread.join(timeout=2.0)

    def set_enabled(self, enabled: bool) -> None:
        self.enabled = bool(enabled)
        if self.enabled:
            self.start()
        else:
            self.stop()

    def set_schedules(self, schedules: List[Dict[str, Any]]) -> None:
        """Replace schedules list. Each schedule is a dict with keys:
        - id: str
        - type: 'once' | 'daily' | 'weekly' | 'interval'
        - datetime: 'YYYY-MM-DD HH:MM' (for once)
        - time: 'HH:MM' or 'HH:MM:SS' (for daily/weekly)
        - days: List[int] (0=Mon .. 6=Sun) (for weekly)
        - interval_seconds: int (for interval)
        - enabled: bool
        - allow_overlap: bool (optional, default False)
        """
        with self._lock:
            self.schedules = [self._normalize_schedule(s) for s in schedules]
            # reset cache to recompute
            self._next_run_cache = {s['id']: None for s in self.schedules}

    def get_schedules(self) -> List[Dict[str, Any]]:
        # Return a copy without transient fields
        with self._lock:
            result: List[Dict[str, Any]] = []
            for s in self.schedules:
                result.append({
                    'id': s['id'],
                    'type': s['type'],
                    'datetime': s.get('datetime'),
                    'time': s.get('time'),
                    'days': list(s.get('days', [])) if s.get('days') is not None else None,
                    'interval_seconds': s.get('interval_seconds'),
                    'enabled': bool(s.get('enabled', True)),
                    'allow_overlap': bool(s.get('allow_overlap', False)),
                })
            return result

    def get_next_runs(self) -> Dict[str, Optional[str]]:
        """For UI: returns ISO strings of next run per schedule id."""
        with self._lock:
            out: Dict[str, Optional[str]] = {}
            for s in self.schedules:
                nid = s['id']
                nr = self._next_run_cache.get(nid) or self._compute_next_run(s)
                out[nid] = nr.isoformat(sep=' ') if nr else None
            return out

    # ---------------- Internal ---------------- #
    def _run_loop(self) -> None:
        while not self._stop_event.is_set():
            try:
                if self.enabled:
                    due: List[Dict[str, Any]] = []
                    now = datetime.now()
                    with self._lock:
                        for s in self.schedules:
                            if not s.get('enabled', True):
                                continue
                            nr = self._next_run_cache.get(s['id'])
                            if nr is None:
                                nr = self._compute_next_run(s)
                                self._next_run_cache[s['id']] = nr
                            if nr and now >= nr:
                                due.append(s)
                    # Execute due outside lock
                    for s in due:
                        self._trigger_if_allowed(s)
                        # Reschedule or disable
                        with self._lock:
                            if s['type'] == 'once':
                                s['enabled'] = False
                                self._next_run_cache[s['id']] = None
                            else:
                                # compute next after now
                                self._next_run_cache[s['id']] = self._compute_next_run(s, base=datetime.now())
                # Sleep with stopable wait
                self._stop_event.wait(self._check_interval_seconds)
            except Exception as e:
                # Do not crash scheduler thread; log minimal
                try:
                    self.controller.update_status(f"Scheduler error: {e}")
                except Exception:
                    pass
                # small backoff to avoid tight loop
                self._stop_event.wait(1.0)

    def _trigger_if_allowed(self, schedule: Dict[str, Any]) -> None:
        allow_overlap = bool(schedule.get('allow_overlap', False))
        # If not allowing overlap and currently playing, skip
        if not allow_overlap and getattr(self.controller, 'is_playing', False):
            return
        # UI-thread safe trigger
        try:
            self.controller.root.after(0, self._start_playback_from_schedule, schedule)
        except Exception:
            # Fallback: call directly (may still be safe since it delegates to thread)
            self._start_playback_from_schedule(schedule)

    def _start_playback_from_schedule(self, schedule: Dict[str, Any]) -> None:
        try:
            # Provide helpful status update
            schedule_label = self._describe_schedule(schedule)
            if hasattr(self.controller, 'status_label'):
                self.controller.update_status(f"Scheduled run: {schedule_label}")
            # Use controller's method that starts playback immediately (no trigger)
            self.controller.start_auto_playback()
        except Exception as e:
            try:
                self.controller.update_status(f"Failed to start scheduled playback: {e}")
            except Exception:
                pass

    def _normalize_schedule(self, s: Dict[str, Any]) -> Dict[str, Any]:
        s = dict(s)
        s.setdefault('id', f"sched-{int(time.time() * 1000)}")
        s.setdefault('enabled', True)
        s.setdefault('allow_overlap', False)
        s_type = s.get('type')
        if s_type not in ('once', 'daily', 'weekly', 'interval'):
            s['type'] = 'once'
        # Normalize lists
        if s.get('days') is None:
            s['days'] = []
        return s

    def _compute_next_run(self, s: Dict[str, Any], base: Optional[datetime] = None) -> Optional[datetime]:
        now = base or datetime.now()
        s_type = s.get('type')
        try:
            if s_type == 'once':
                dt_str = s.get('datetime')
                if not dt_str:
                    return None
                dt = self._parse_datetime(dt_str)
                return dt if dt and dt > now else None

            if s_type == 'daily':
                t = self._parse_time(s.get('time'))
                if not t:
                    return None
                candidate = now.replace(hour=t.hour, minute=t.minute, second=t.second, microsecond=0)
                if candidate <= now:
                    candidate += timedelta(days=1)
                return candidate

            if s_type == 'weekly':
                t = self._parse_time(s.get('time'))
                days: List[int] = [int(d) for d in (s.get('days') or []) if isinstance(d, (int, str))]
                days = [int(d) for d in days if 0 <= int(d) <= 6]
                if not t or not days:
                    return None
                today_wd = now.weekday()  # Mon=0 .. Sun=6
                # Search next occurrence including today
                for delta in range(0, 8):
                    wd = (today_wd + delta) % 7
                    if wd in days:
                        candidate = (now + timedelta(days=delta)).replace(
                            hour=t.hour, minute=t.minute, second=t.second, microsecond=0
                        )
                        if candidate > now:
                            return candidate
                # Fallback one week ahead
                delta_to_first = (min(days) - today_wd) % 7 or 7
                candidate = (now + timedelta(days=delta_to_first)).replace(
                    hour=t.hour, minute=t.minute, second=t.second, microsecond=0
                )
                return candidate

            if s_type == 'interval':
                interval_seconds = int(s.get('interval_seconds') or 0)
                if interval_seconds <= 0:
                    return None
                return now + timedelta(seconds=interval_seconds)
        except Exception:
            return None
        return None

    @staticmethod
    def _parse_time(value: Optional[str]) -> Optional[dt_time]:
        if not value:
            return None
        try:
            parts = value.strip().split(":")
            if len(parts) == 2:
                h, m = int(parts[0]), int(parts[1])
                return datetime.now().replace(hour=h, minute=m, second=0, microsecond=0).time()
            if len(parts) == 3:
                h, m, s = int(parts[0]), int(parts[1]), int(parts[2])
                return datetime.now().replace(hour=h, minute=m, second=s, microsecond=0).time()
        except Exception:
            return None
        return None

    @staticmethod
    def _parse_datetime(value: Optional[str]) -> Optional[datetime]:
        if not value:
            return None
        value = value.strip()
        # Accept formats: 'YYYY-MM-DD HH:MM' or ISO-like 'YYYY-MM-DD HH:MM:SS'
        for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        # Try ISO parse
        try:
            return datetime.fromisoformat(value)
        except Exception:
            return None

    @staticmethod
    def _describe_schedule(s: Dict[str, Any]) -> str:
        s_type = s.get('type')
        if s_type == 'once':
            return f"Once at {s.get('datetime')}"
        if s_type == 'daily':
            return f"Daily at {s.get('time')}"
        if s_type == 'weekly':
            days = s.get('days') or []
            days_str = ",".join(str(d) for d in days)
            return f"Weekly at {s.get('time')} on [{days_str}]"
        if s_type == 'interval':
            return f"Every {s.get('interval_seconds')}s"
        return "Scheduled"
