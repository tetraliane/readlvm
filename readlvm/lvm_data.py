from __future__ import annotations


class LvmData:
    _title: str
    _header: dict[str, str]
    _data_labels: list[str]
    _data: list[list[str]]

    # constructors

    def __init__(
        self,
        title: str,
        header: dict[str, str],
        data_labels: list[str],
        data: list[list[str]],
    ) -> None:
        self._title = title
        self._header = header
        self._data_labels = data_labels
        self._data = data

    @classmethod
    def read(cls, filename: str) -> LvmData:
        ins = cls("", dict(), [], [])
        with open(filename) as f:
            ins._title = f.readline().strip()

            # ヘッダーとデータラベルを読み取る。
            data_count = 0
            while True:
                line = f.readline()
                if line.startswith("***"):
                    continue
                if len(line.strip()) == 0:
                    continue

                spl = line.split()
                if len(spl) == 2:
                    ins._header[spl[0]] = spl[1]
                else:
                    ins._data_labels = spl
                    data_count = len(spl)
                    break

            # データを読み取る。
            for line in f:
                if line.startswith("***"):
                    continue
                if len(line.strip()) == 0:
                    continue

                # 先頭が省略されて空白になっているのを検出するため、先頭に文字を入れてから分割する。
                spl = ("^" + line).split()
                spl[0] = spl[0][1:]
                # 末尾を空白を埋める。
                spl += [""] * max(data_count - len(spl), 0)

                ins._data.append(spl)

        return ins

    # getters

    def title(self) -> str:
        return self._title

    def header(self) -> dict[str, str]:
        return self._header.copy()

    def data_labels(self) -> list[str]:
        return self._data_labels.copy()

    def data(self) -> list[list[str]]:
        # Deepcopy the data
        return list(map(lambda row: row.copy(), self._data))

    # other methods

    def into_yaml(self) -> object:
        return {
            "title": self.title(),
            "header": self.header(),
            "data_labels": self.data_labels(),
            "data": self.data(),
        }

    def compress_data(self, col_index: int) -> LvmData:
        label = self.data_labels()[col_index]
        out = LvmData(self.title(), self.header(), [label, "count_of_" + label], [])

        begin = 0
        for i in range(1, len(self._data)):
            prev = self._data[i - 1][col_index]
            current = self._data[i][col_index]
            if prev != current:
                out._data.append([prev, i - begin])
                begin = i
        out._data.append([self._data[-1][col_index], len(self._data) - begin])

        return out
