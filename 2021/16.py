from __future__ import annotations

import sys
from typing import Optional

sys.setrecursionlimit(1500)  # Father, forgive them; for they know not what they do

data_hex = open("16.txt").read().strip()


class PacketDecoder:
    def __init__(self, hexadecimal: str):
        self.hexadecimal = hexadecimal
        self.binary = bin(int(hexadecimal, 16))[2:]
        if mod := len(self.binary) % 4:
            self.binary = self.binary.zfill(len(self.binary) + 4 - mod)

        self.packets: list[Packet] = []
        self._decode_binary(binary=self.binary)

    @property
    def packet_values(self) -> list[int]:
        return [packet.value for packet in self.packets]

    @property
    def packet_version_numbers(self) -> list[int]:
        return [packet.version for packet in self.packets]

    def _decode_binary(self, binary: str):
        main_packet = Packet(binary=binary)
        self._decode_excess_packets(packet=main_packet)

    def _decode_excess_packets(self, packet: Packet):
        self.packets.append(packet)
        if packet.excess_packet:
            self._decode_excess_packets(packet.excess_packet)

    def __repr__(self):
        return f"PacketDecoder(hexadecimal='{self.hexadecimal}')"


class Packet:
    def __init__(self, binary: str):
        self.binary: str = binary
        self.value: int = 0
        self.excess_packet: Optional[Packet] = None
        self._decode()

    @property
    def version(self) -> int:
        return int(self.binary[0:3], base=2)

    @property
    def type_id(self) -> int:
        return int(self.binary[3:6], base=2)

    @property
    def length_type_id(self) -> Optional[int]:
        return int(self.binary[6])

    def _decode(self):
        if self.type_id == 4:
            self.value, excess_binary = self._parse_literal_packet(binary=self.binary[6:])
            self.excess_packet = self._parse_excess_packet(binary=excess_binary)
        elif self.length_type_id == 0:
            packet_length = 15
            excess_binary = self.binary[7 + packet_length :]
            self.excess_packet = self._parse_excess_packet(binary=excess_binary)
        elif self.length_type_id == 1:
            packet_length = 11
            excess_binary = self.binary[7 + packet_length :]
            self.excess_packet = self._parse_excess_packet(binary=excess_binary)

    @staticmethod
    def _parse_literal_packet(binary: str) -> tuple[int, str]:
        literal_value = ""
        for i in range(len(binary) // 5):
            slice_start, slice_end = i * 5 + 1, i * 5 + 5
            literal_value += binary[slice_start:slice_end]
            if binary[i * 5] == "0":
                return int(literal_value, base=2), binary[slice_end:]

    @classmethod
    def _parse_excess_packet(cls, binary: str) -> Optional[Packet]:
        if binary.replace("0", ""):
            return cls(binary=binary)

    def __repr__(self):
        return f"Packet(binary='{self.binary}')"

    def __str__(self):
        return f"Packet({self.binary})\n\tvalue - {self.value}\n\texcess - {self.excess_packet}"


decoder = PacketDecoder(hexadecimal=data_hex)

# print("PACKETS: ", decoder.packets)
print("VALUES: ", decoder.packet_values)
print("VERSIONS: ", decoder.packet_version_numbers)
print("PART ONE", sum(decoder.packet_version_numbers))
