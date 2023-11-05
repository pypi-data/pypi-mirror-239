# Overview
A pure Python interface to the NTP shared memory segment with no external
dependencies.

The only platform-dependent part of this library is the `SHM_CREAT` constant,
which seems to always be the octal value of 01000 (Linux and BSDs). Technically
the size of `time_t` is also platform-dependent, but it's 2021 and this should
be 64 bit everywhere.

# Prerequisites
Python: 3.7+

OSs: Posix-compliant with the System V shared memory interface.

This uses `ctypes` for direct access to memory and shared memory routines. This
will dynamically load the system's C library to access `shmget()` and `shmat()`
functions.

# Usage

## NTP Shared Memory
The `NtpShm` class wraps up access to the NTP shared memory segments. See the
[NTP documentation](https://docs.ntpsec.org/latest/driver_shm.html) for
information on the contents of this memory and how to safely access it.

Example use:
```python
from ntp_shm import NtpShm

seg = NtpShm(segment=0)

# Access copies of the memory segment (ShmTime) through read()/write()
shm_time = seg.read()
shm_time.count += 1
shm_time.clock_time_sec = 42
# ...
seg.write(shm_time)

# Dynamic, direct access (by ref) through .ref
shm_time = seg.ref  # Or just use seg.ref directly
shm_time.count += 1
shm_time.clock_time_sec = 42
# ...
```

The `ShmTime` object is a `ctypes` structure with a few extra properties for
convenience, and with fields renamed slightly to be more pythonic. The
convenience properties can be used to set or get the clock or receive times
using `datetime` objects or integer time in nanoseconds.

```python
>>> shm_time = seg.ref
>>> seg.ref.receive_dt
datetime.datetime(2021, 9, 6, 13, 45, 3, 495830, tzinfo=datetime.timezone.utc)
>>> seg.ref.receive_dt
datetime.datetime(2021, 9, 6, 13, 45, 4, 440210, tzinfo=datetime.timezone.utc)
>>> shm_time.clock_ns
1630935919000000000
```

Keep in mind that the `datetime` representation is only accurate to the
microsecond.

**Important**: Direct access to the shared memory segment suffers from race
conditions. Since the time values are split up across multiple fields, these
may be modified in between field reads leading to consumers reading corrupted
values.

The NTP documentation (above) specifies two different methods of updating and
reading from the shared memory segment to avoid this issue. Writing via mode 1
is implemented in the `ShmTime.update()` method. This can be used to update
the clock and receive times:

```python
from ntp_shm import util, NtpShm

seg = NtpShm()

clock_time_ns = some_function_that_gives_integer_nanoseconds()
receive_time_ns = util.datetime_to_ns(datetime.datetime.now())

seg.update(clock_time_ns, receive_time_ns)
```

Since Python lacks memory barriers or cache synchronization controls, its still
not 100% guaranteed that the `update()` method will be issue free.

## NTP Bridge
Included is a utility command: `ntp-shm bridge`. This acts as a very basic
NMEA0183 bridge to NTP shared memory. It reads lines from a file input, looking
for and parsing valid GPRMC NMEA sentences. Valid times, after a small holdoff
to allow for stabilization, are passed to the NTP shared memory segment.

The NMEA sentences must come from a file-like device, such as a character
device or pipe (stdin). For GPSs connected to a serial tty device, use `stty`
to configure the device for direct access. Alternatively, use one of many
applications to handle the serial interface and pipe the output to `ntp-shm
bridge`.

Example tty setup for raw access (on FreeBSD).
```shell
stty -f /dev/ttyu1.init raw 9600
```

Test the tty configuration using `cat /dev/ttyu1`. The output should be
smooth, without extra blank lines or non-printable characters.

To bridge the NMEA data on `ttyu1` to segment 0:
```shell
ntp-shm bridge -p /dev/ttyu1 -s 0
```

To create a persistent process, consider using `daemon` (FreeBSD) or
`daemonize` (Linux) and your system's service manager.

# Installation
From pypi:
```shell
pip install ntp-shm
```

From your local checkout:
```shell
pip install [--user] .
```

or

```shell
python setup.py install [--user]
```
