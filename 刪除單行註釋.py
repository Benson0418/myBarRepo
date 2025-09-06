#!/usr/bin/env python3
"""
strip_cpp_line_comments.py

移除 C/C++ 程式碼中的單行註解 // ... ，但保留出現在字串、字元、區塊註解、以及 raw string literal (R"...") 裡面的 //。

用法:
    python strip_cpp_line_comments.py input.cpp > output.cpp
或
    python strip_cpp_line_comments.py -i input.cpp   # 會備份成 input.cpp.bak 再就地覆寫
"""

import sys
import re
from pathlib import Path

# Regex to detect raw-string prefix at current index: optional prefix (u8|u|U|L) then R"delim(
RAW_PREFIX_RE = re.compile(r'^(?:u8|U|u|L)?R"(?P<delim>[^()\n\r]*)\(' , re.ASCII)

def remove_cpp_single_line_comments(text: str) -> str:
    i = 0
    n = len(text)
    out_chars = []

    while i < n:
        ch = text[i]

        # 1) double-quote string literal
        if ch == '"':
            out_chars.append(ch)
            i += 1
            while i < n:
                c = text[i]
                out_chars.append(c)
                i += 1
                if c == '\\':                      # escape next char
                    if i < n:
                        out_chars.append(text[i])
                        i += 1
                elif c == '"':                     # end of string
                    break
            continue

        # 2) single-quote char literal
        if ch == "'":
            out_chars.append(ch)
            i += 1
            while i < n:
                c = text[i]
                out_chars.append(c)
                i += 1
                if c == '\\':                      # escaped char inside ''
                    if i < n:
                        out_chars.append(text[i])
                        i += 1
                elif c == "'":                     # end of char literal
                    break
            continue

        # 3) raw-string literal (may span lines)
        # Try regex at the remaining substring
        m = RAW_PREFIX_RE.match(text[i:])
        if m:
            delim = m.group('delim')  # can be empty
            # compute the exact start length of the prefix (like u8R"delim(
            prefix_len = m.end()  # number of chars matched
            # append the prefix as-is
            out_chars.append(text[i:i+prefix_len])
            i += prefix_len
            # find end sequence: )delim"
            end_seq = ')' + delim + '"'
            j = text.find(end_seq, i)
            if j == -1:
                # Unterminated raw string: append rest and break
                out_chars.append(text[i:])
                break
            else:
                # include everything up to and including the end_seq
                out_chars.append(text[i:j+len(end_seq)])
                i = j + len(end_seq)
            continue

        # 4) block comment /* ... */
        if ch == '/' and i+1 < n and text[i+1] == '*':
            # copy the block comment as-is
            end = text.find('*/', i+2)
            if end == -1:
                # unterminated block comment: append rest and break
                out_chars.append(text[i:])
                break
            else:
                out_chars.append(text[i:end+2])
                i = end + 2
            continue

        # 5) single-line comment // -> remove until newline (but keep newline)
        if ch == '/' and i+1 < n and text[i+1] == '/':
            # skip until end of line but keep the newline if present
            i += 2
            while i < n and text[i] not in '\r\n':
                i += 1
            # if newline sequence CRLF or LF, keep it
            if i < n and text[i] == '\r':
                out_chars.append('\r')
                i += 1
                if i < n and text[i] == '\n':
                    out_chars.append('\n')
                    i += 1
            elif i < n and text[i] == '\n':
                out_chars.append('\n')
                i += 1
            # else EOF -> nothing to append
            continue

        # default: copy char
        out_chars.append(ch)
        i += 1

    return ''.join(out_chars)


def main(argv):
    import argparse
    p = argparse.ArgumentParser(description="移除 C/C++ 單行註解 // (保留字串、字元、區塊註解與 raw-string)")
    p.add_argument('infile', nargs='?', help='輸入檔案，若未給則從 stdin 讀取')
    p.add_argument('-i', '--inplace', action='store_true', help='就地覆寫 infile（會先備份為 infile.bak）')
    args = p.parse_args(argv)

    if args.infile:
        path = Path(args.infile)
        text = path.read_text(encoding='utf-8')
    else:
        text = sys.stdin.read()

    new_text = remove_cpp_single_line_comments(text)

    if args.infile and args.inplace:
        bak = path.with_suffix(path.suffix + '.bak')
        # 在不覆寫同名備份的情況下記得備份
        bak.write_text(text, encoding='utf-8')
        path.write_text(new_text, encoding='utf-8')
        print(f'覆寫完成，已備份原檔為: {bak}', file=sys.stderr)
    else:
        # 輸出到 stdout
        sys.stdout.write(new_text)


if __name__ == '__main__':
    main(sys.argv[1:])
