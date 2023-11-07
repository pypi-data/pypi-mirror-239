import random
import typing
import unittest
from datetime import date, datetime, timezone
from ipaddress import IPv4Address, IPv6Address, ip_address
from json import JSONDecoder
from timeit import timeit
from typing import Any, Callable, Tuple, Union
from uuid import UUID

from tsv.helper import is_union_like, types_to_format_str, unescape
from tsv.parser import parse_line, parse_record


def parse_datetime(s: bytes) -> datetime:
    return (
        datetime.fromisoformat(s.decode("ascii").replace("Z", "+00:00"))
        .astimezone(timezone.utc)
        .replace(tzinfo=None)
    )


def parse_date(s: bytes) -> date:
    return date.fromisoformat(s.decode("ascii"))


def parse_str(s: bytes) -> str:
    return unescape(s).decode("utf-8")


def parse_uuid(s: bytes) -> UUID:
    return UUID(s.decode("ascii"))


def parse_ipv4addr(s: bytes) -> IPv4Address:
    return IPv4Address(s.decode("ascii"))


def parse_ipv6addr(s: bytes) -> IPv6Address:
    return IPv6Address(s.decode("ascii"))


def parse_ipaddr(s: bytes) -> IPv4Address:
    return ip_address(s.decode("ascii"))


DECODER = JSONDecoder()


def parse_json(s: bytes) -> Any:
    return DECODER.decode(s.decode("utf-8"))


def type_to_converter(typ: type) -> Callable[[bytes], Any]:
    if typ is bool:
        return bool
    elif typ is int:
        return int
    elif typ is float:
        return float
    elif typ is str:
        return parse_str
    elif typ is datetime:
        return parse_datetime
    elif typ is date:
        return parse_date
    elif typ is UUID:
        return parse_uuid
    elif typ is bytes:
        return bytes
    elif typ is IPv4Address:
        return parse_ipv4addr
    elif typ is IPv6Address:
        return parse_ipv6addr
    elif typ is list or typ is dict:
        return parse_json

    if is_union_like(typ):
        args = typing.get_args(typ)
        if len(args) == 2 and IPv4Address in args and IPv6Address in args:
            return parse_ipaddr

    raise TypeError(f"conversion for type `{typ}` is not supported")


def types_to_converters(fields: Tuple[type, ...]) -> Tuple[Callable[[bytes], Any], ...]:
    return tuple(type_to_converter(typ) for typ in fields)


def process_record_python(
    converters: Tuple[Callable[[bytes], Any], ...], tsv_record: tuple
) -> tuple:
    return tuple(
        converter(field) if field != b"\N" else None
        for (converter, field) in zip(converters, tsv_record)
    )


def process_line_python(
    converters: Tuple[Callable[[bytes], Any], ...], tsv_line: bytes
) -> tuple:
    return tuple(
        converter(field) if field != b"\N" else None
        for (converter, field) in zip(converters, tsv_line.split(b"\t"))
    )


def process_record_c(converters: str, tsv_record: tuple) -> tuple:
    return parse_record(converters, tsv_record)


def process_line_c(converters: str, tsv_line: bytes) -> tuple:
    return parse_line(converters, tsv_line)


class Tester:
    tsv_types: Tuple[type, ...]
    tsv_record: Tuple[Any, ...]
    tsv_line: bytes
    converters: Tuple[Callable[[bytes], Any], ...]
    format_str: str

    def __init__(
        self, tsv_types: Tuple[type, ...], tsv_record: Tuple[Any, ...]
    ) -> None:
        self.tsv_types = tsv_types
        self.tsv_record = tsv_record
        self.tsv_line = b"\t".join(self.tsv_record)
        self.converters = types_to_converters(tuple(typ for typ in self.tsv_types))
        self.format_str = types_to_format_str(tuple(typ for typ in self.tsv_types))


class TestPerformance(unittest.TestCase):
    iterations: int = 100000

    tsv_types: tuple = (
        str,
        datetime,
        float,
        int,
        str,
        str,
        UUID,
        bool,
        IPv4Address,
        IPv6Address,
        Union[IPv4Address, IPv6Address],
        list,
        dict,
    )
    tsv_record: tuple = (
        "árvíztűrő tükörfúrógép".encode("utf-8"),
        b"1989-10-23T23:59:59Z",
        b"0.5",
        b"-56",
        "árvíztűrő \\r\\n tükörfúrógép".encode("utf=8"),
        b"Etiam pulvinar diam et diam lacinia, in consectetur neque consequat. Cras pharetra ut metus ac lobortis. Vestibulum interdum euismod odio sed cursus. Integer orci magna, mollis et mattis non, dignissim eu ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Maecenas sit amet lacinia enim. Quisque porttitor turpis eu tristique cursus. Pellentesque aliquam dui sit amet laoreet porta.",
        str(UUID("f81d4fae-7dec-11d0-a765-00a0c91e6bf6")).encode("ascii"),
        b"true",
        b"192.0.2.0",
        b"2001:DB8:0:0:8:800:200C:417A",
        b"2001:DB8:0:0:8:800:200C:417A",
        b"[1,2,3,4,5,6,7,8,9]",
        b'{"string": "value", "integer": 82, "float": 23.45}',
    )

    tester: Tester

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.tester = Tester(self.tsv_types, self.tsv_record)

    def test_parse_record(self) -> None:
        self.assertEqual(
            process_record_python(self.tester.converters, self.tsv_record),
            process_record_c(self.tester.format_str, self.tsv_record),
        )

        print()
        print("Parsing records...")
        time_py = timeit(
            lambda: process_record_python(self.tester.converters, self.tsv_record),
            number=self.iterations,
        )
        time_c = timeit(
            lambda: process_record_c(self.tester.format_str, self.tsv_record),
            number=self.iterations,
        )
        percent = 100 * (1 - time_c / time_py)
        print(f"Python interpreter took {time_py:.2f} s")
        print(f"C extension took {time_c:.2f} s")
        print(f"{percent:.2f}% savings")

    def test_parse_line(self) -> None:
        self.assertEqual(
            process_line_python(self.tester.converters, self.tester.tsv_line),
            process_line_c(self.tester.format_str, self.tester.tsv_line),
        )

        print()
        print("Parsing lines...")
        time_py = timeit(
            lambda: process_line_python(self.tester.converters, self.tester.tsv_line),
            number=self.iterations,
        )
        time_c = timeit(
            lambda: process_line_c(self.tester.format_str, self.tester.tsv_line),
            number=self.iterations,
        )
        percent = 100 * (1 - time_c / time_py)
        print(f"Python interpreter took {time_py:.2f} s")
        print(f"C extension took {time_c:.2f} s")
        print(f"{percent:.2f}% savings")


class TestPerformanceManyFields(unittest.TestCase):
    iterations: int = 100000

    def test_parse_many_fields(self) -> None:
        tsv_types: Tuple[type, ...] = tuple([int] * 100)
        tsv_record: Tuple[Any, ...] = tuple(
            str(random.randint(0, 10000)).encode("ascii") for i in range(100)
        )
        tester = Tester(tsv_types, tsv_record)
        self.assertEqual(
            process_line_python(tester.converters, tester.tsv_line),
            process_line_c(tester.format_str, tester.tsv_line),
        )

        print()
        print("Parsing lines with many fields...")
        time_py = timeit(
            lambda: process_line_python(tester.converters, tester.tsv_line),
            number=self.iterations,
        )
        time_c = timeit(
            lambda: process_line_c(tester.format_str, tester.tsv_line),
            number=self.iterations,
        )
        percent = 100 * (1 - time_c / time_py)
        print(f"Python interpreter took {time_py:.2f} s")
        print(f"C extension took {time_c:.2f} s")
        print(f"{percent:.2f}% savings")


if __name__ == "__main__":
    unittest.main()
