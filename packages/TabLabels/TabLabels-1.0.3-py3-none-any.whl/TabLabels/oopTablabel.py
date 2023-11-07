import re
import os
import json

class DataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def is_valid_path(self):
        return os.path.exists(self.file_path)

    def load_data(self):
        if self.is_valid_path():
            with open(self.file_path, "r", encoding="utf-8") as input_file:
                self.contents = input_file.read()
        else:
            print(f"'{self.file_path}' không phải là một đường dẫn hợp lệ.")
            return False

    def phase_2(self, qq):
        lst_kq = []
        z = qq.split(">")
        z = list(map(lambda x: x + ">", z))[:-1]
        for i in z:
            if "</td>" in i and "</td>" != i:
                z = i.split("</td>")
                z[-1] = "</td>"
                for j in z:
                    lst_kq.append(j)
            else:
                lst_kq.append(i)
        e = []
        for i in range(len(lst_kq) - 1):
            if lst_kq[i] == "<td>" and lst_kq[i + 1] == "</td>":
                e.append(lst_kq[i])
                e.append("")
            elif lst_kq[i].startswith("<") and lst_kq[i+1] == "</td>":
                e.append(lst_kq[i])
                e.append("")
            else:
                e.append(lst_kq[i])
        return e

    def loai_phan_thua(self, s):
        s = s.replace("<b>", "")
        k = ["</sup>", "<sup>", "<b> ", "</b>", '<tbody>', '</tbody>', '</i>', "<i>", "</body>", "<body>",
             "</html>", "<html>", "</sub>", "<sub>"]
        for item in k:
            s = s.replace(item, "")
        # add key and value special Character at here
        Spec = {"&quot;":"\""}
        for key, value in Spec.items():
                s = s.replace(key, value)
        return s

    def ki_tu_html_special_limited(self, e):
        m = []
        for i in range(len(e)):
            if e[i] != e[i].split(" ")[0] and e[i] != " ":
                if e[i].startswith("<") and e[i].endswith(">"):
                    text = e[i]
                    z = e[i].split("d")
                    z = [z[1].split(">")[0]]
                    z.append(">")
                    split_text = text.split(" ")
                    result = []
                    for idx, item in enumerate(split_text):
                        result.append(item)
                        if idx < len(split_text) - 1:
                            result.append(" ")
                    v = result[0:1] + z
                    for j in v:
                        m.append(j)
                    continue
                m.append(e[i])
            else:
                if e[i] != "<table>" and e[i] != "</table>":
                    m.append(e[i])
        return m

    def process_data(self, line):
        mph = re.split(r'\t', line)
        content = mph[1]
        img = mph[0]
        phan_du = self.loai_phan_thua(content)
        mph = self.ki_tu_html_special_limited(self.phase_2(phan_du))
        html_list = [item for item in mph if item.endswith(">") or item.endswith('"') or item.endswith("td")]
        list_Cell = [item for item in mph if item not in html_list]

        cell1 = [x for x in html_list]
        cell1 = [x.replace('\\"', '"') if '\\"' in x else x for x in cell1]

        Cells = []
        for i in list_Cell:
            cell = {"tokens": [x for x in i], "bbox": [[[0, 0], [0, 0]]]}
            Cells.append(cell)

        cell2 = Cells

        cell3 = "<html><body>" + content + "</body></html>"

        data = {
            "structure": {"tokens": cell1},
            "cells": cell2
        }

        return {"filename": img, 'html': data, 'gt': cell3}

    def process_file(self, output_file_path="outputZ.txt"):
        self.load_data()
        if not self.contents:
            return

        with open(output_file_path, "w", encoding="utf-8") as output_file:
            lines = re.split(r'\n', self.contents)
            for line in lines:
                data = self.process_data(line)
                json.dump(data, output_file, ensure_ascii=False)
                output_file.write("\n")
        print("File đã được lưu với đường dẫn " + output_file_path)

def main():
    file_path = input("Tên file:... ")
    data_processor = DataProcessor(file_path)
    data_processor.process_file()
if __name__ == "__main__":
  main()
  print("file has been save")

#if __name__ == "__main__":
#    main()

